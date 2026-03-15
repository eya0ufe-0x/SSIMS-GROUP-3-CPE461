import contextlib
from http.client import HTTPConnection
from http.client import HTTPException
from http.client import ResponseNotReady
from pathlib import Path
import socket
from socket import timeout as SocketTimeout
import subprocess
import sys
import time
from typing import Iterable

from playwright.sync_api import Browser
from playwright.sync_api import Page
from playwright.sync_api import Playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


HOST = "127.0.0.1"
PREFERRED_PORT = 8000
SERVER_STARTUP_TIMEOUT_SECONDS = 30


def is_port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.3)
        return sock.connect_ex((host, port)) == 0


def find_free_port(host: str, preferred_port: int) -> int:
    if not is_port_open(host, preferred_port):
        return preferred_port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        free_port = sock.getsockname()[1]
    return free_port


def python_has_modules(python_executable: str, modules: Iterable[str]) -> bool:
    probe = (
        "import importlib.util, sys; "
        f"mods={tuple(modules)!r}; "
        "sys.exit(0 if all(importlib.util.find_spec(m) is not None for m in mods) else 1)"
    )
    result = subprocess.run(
        [python_executable, "-c", probe],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def pick_server_python() -> str:
    workspace_python = str((Path(__file__).resolve().parent / "venv" / "bin" / "python"))
    candidates = [sys.executable, workspace_python, "python3"]
    for candidate in candidates:
        if candidate != "python3" and not Path(candidate).exists():
            continue
        if python_has_modules(candidate, ("uvicorn", "fastapi", "sqlmodel")):
            return candidate
    raise RuntimeError("No Python interpreter with uvicorn/fastapi/sqlmodel available for server startup")


def wait_for_server(host: str, port: int, timeout_seconds: int) -> None:
    deadline = time.time() + timeout_seconds
    last_error: Exception | None = None
    while time.time() < deadline:
        connection = HTTPConnection(host, port, timeout=2)
        try:
            connection.request("GET", "/")
            response = connection.getresponse()
            status_code = response.status
            _ = response.read()
            if status_code == 200:
                return
            last_error = RuntimeError(f"Unexpected status code from /: {status_code}")
        except (ConnectionError, HTTPException, OSError, ResponseNotReady, SocketTimeout) as exc:
            last_error = exc
        finally:
            connection.close()
        time.sleep(0.5)
    raise RuntimeError(
        f"Server did not become ready within {timeout_seconds}s at http://{host}:{port}. Last error: {last_error}"
    )


def stop_server(server_process: subprocess.Popen[str]) -> None:
    if server_process.poll() is not None:
        return
    server_process.terminate()
    try:
        _ = server_process.wait(timeout=8)
    except subprocess.TimeoutExpired:
        server_process.kill()
        _ = server_process.wait(timeout=5)


def run_e2e() -> None:
    server_python = pick_server_python()
    port = find_free_port(HOST, PREFERRED_PORT)
    base_url = f"http://{HOST}:{port}"
    print(f"[INFO] Starting uvicorn on {base_url} using {server_python}")
    server_process = subprocess.Popen(
        [
            server_python,
            "-m",
            "uvicorn",
            "server.main:app",
            "--host",
            HOST,
            "--port",
            str(port),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    browser: Browser | None = None
    playwright: Playwright | None = None

    try:
        wait_for_server(HOST, port, SERVER_STARTUP_TIMEOUT_SECONDS)
        print("[PASS] Server started and is reachable")
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        page: Page = browser.new_page()

        page.goto(f"{base_url}/", wait_until="networkidle")
        page.wait_for_selector("text=Welcome to SSIMS", timeout=10_000)
        print("[PASS] Step 1: Home page loaded with expected content")

        page.get_by_role("button", name="Get Started").click()
        page.wait_for_url(f"{base_url}/static/search.html", timeout=10_000)
        print("[PASS] Step 2: Navigated to /static/search.html")

        page.select_option("#course", "Computer Engineering")
        page.select_option("#location", "Lagos")
        print("[PASS] Step 3: Selected course and location")

        page.locator("#submit").click()
        page.wait_for_url(f"{base_url}/static/results.html**", timeout=10_000)
        print("[PASS] Step 4: Navigated to /static/results.html")

        page.wait_for_selector(".company-card", timeout=15_000)
        cards = page.locator(".company-card")
        card_count: int = cards.count()
        if card_count < 1:
            raise AssertionError("Expected at least one result card, but none were found.")
        print(f"[PASS] Step 5: Results loaded with {card_count} card(s)")

        cards.nth(0).locator("a.details-button").click()
        page.wait_for_url(f"{base_url}/static/details.html**", timeout=10_000)
        print("[PASS] Step 6: Navigated to /static/details.html")

        page.wait_for_selector("#company-name", timeout=10_000)
        company_name = page.locator("#company-name").inner_text().strip()
        if not company_name:
            raise AssertionError("Company name is empty on details page.")
        apply_button = page.locator("#apply-button")
        if not apply_button.is_visible():
            raise AssertionError("Apply Now button is not visible on details page.")

        print(f"[PASS] Step 7: Company Name ('{company_name}') and Apply Now button are visible")
        print("\n[SUCCESS] End-to-end user journey passed: Home -> Search -> Results -> Details")

    except PlaywrightTimeoutError as exc:
        print(f"\n[FAIL] Playwright timeout: {exc}")
        raise
    except Exception as exc:
        print(f"\n[FAIL] E2E test failed: {exc}")
        raise
    finally:
        if browser is not None:
            with contextlib.suppress(Exception):
                browser.close()
        if playwright is not None:
            with contextlib.suppress(Exception):
                playwright.stop()
        stop_server(server_process)
        if server_process.stdout is not None:
            server_output = server_process.stdout.read()
            if server_output.strip():
                print("\n[SERVER LOG OUTPUT]")
                print(server_output)


if __name__ == "__main__":
    try:
        run_e2e()
    except Exception as exc:
        print(f"\n[ERROR] Unhandled exception: {exc}", file=sys.stderr)
        sys.exit(1)
