# Backend Migration & Feature Implementation Plan

## TL;DR
> **Quick Summary**: Transform the static frontend into a dynamic FastAPI web application. Migrate files to `client/` and `server/` structure, implement a SQLite database with SQLModel, and create a search-based flow for SIWES opportunities.
> 
> **Deliverables**:
> - Reorganized Project Structure (`client/`, `server/`)
> - FastAPI Backend with SQLite Database & Seeding Script
> - 2 API Endpoints (`GET /api/companies`, `GET /api/companies/{id}`)
> - Updated Frontend: Search Page (was login.html), Results Page, Details Page
> - Automated Tests (Backend `pytest`, Frontend `playwright`)
> 
> **Estimated Effort**: Medium
> **Parallel Execution**: YES - 5 waves
> **Critical Path**: Scaffold → Models → API → Frontend Pages → Integration

---

## Context

### Original Request
- Create a simple Python backend (FastAPI selected) for SIWES opportunities.
- Update `login.html` to be a Search Filter (Course + Location only).
- "Upload manually scaffolded data" -> Implemented as a JSON seed script.
- Restructure project into `client/` and `server/`.
- Create results and details pages to display data.

### Interview Summary
**Key Decisions**:
- **Framework**: FastAPI + SQLModel (Sync SQLite)
- **Data**: Read-only API populated via `seed.py` from `data.json`.
- **Frontend**: Vanilla JS + Fetch API (SPA-lite).
- **Navigation**: `index.html` (Landing) → `search.html` (Filter) → `results.html` (List) → `details.html` (Single).

### Metis Review
**Guardrails Applied**:
- **No Auth/User Storage**: Strictly a search tool.
- **No Complex Build**: Vanilla JS/CSS only.
- **Thread Safety**: `check_same_thread=False` for SQLite.
- **Startup**: Use `lifespan` context manager for seeding.
- **Testing**: In-memory SQLite for `pytest`.

---

## Work Objectives

### Core Objective
Convert static prototype into a functional search application for SIWES placements.

### Concrete Deliverables
- `server/main.py`: FastAPI app serving API + Static files.
- `server/models.py`: SQLModel definition for `Company`.
- `data.json`: Seed data (20+ companies).
- `client/search.html`: Refactored `login.html`.
- `client/results.html`: New page fetching from API.
- `client/details.html`: New page for single company.

### Definition of Done
- [ ] Backend serves `client/index.html` at root `/`.
- [ ] API returns JSON data from SQLite database.
- [ ] Search filters work for Course and Location.
- [ ] Clicking a company shows correct details.
- [ ] All `pytest` tests pass.

### Must Have
- **SQLModel** for ORM.
- **Lifespan** event for DB seeding.
- **Case-insensitive** search.
- **Preserved Styling**: Keep existing CSS/Fonts/Images.

### Must NOT Have
- User registration/login.
- Admin interface.
- Javascript frameworks (React/Vue).
- Docker/Deployment config.

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed.

### Test Decision
- **Infrastructure**: None currently -> **Setup Pytest**.
- **Strategy**: TDD (Write tests first, then implementation).
- **Backend**: `pytest` + `TestClient` + In-memory SQLite.
- **Frontend**: `playwright` for navigation and DOM assertions.

### QA Policy
Every task MUST include agent-executed QA scenarios.
- **Backend**: `pytest server/tests/...`
- **Frontend**: `playwright` scripts or `curl` validation.

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Scaffold & Structure):
├── Task 1: Project Restructure & Cleanup [quick]
├── Task 2: Python Environment Setup (requirements.txt) [quick]
└── Task 3: Test Infrastructure Setup (conftest.py) [quick]

Wave 2 (Backend Core - TDD):
├── Task 4: Database & Models Implementation [deep]
├── Task 5: Seed Data & Script [quick]
└── Task 6: API Endpoints Implementation [deep]

Wave 3 (Server Integration):
├── Task 7: FastAPI App & Static Serving [quick]
└── Task 8: Landing Page (index.html) Migration [quick]

Wave 4 (Frontend Feature Implementation):
├── Task 9: Search Page (login.html refactor) [visual-engineering]
├── Task 10: Results Page Implementation [visual-engineering]
└── Task 11: Details Page Implementation [visual-engineering]

Wave 5 (Final Verification):
├── Task 12: End-to-End Integration Test [deep]
└── Task 13: Final Code Quality & Cleanup [unspecified-high]

Critical Path: T1 → T4 → T6 → T7 → T9 → T10 → T11
```

---

## TODOs

- [x] 1. Project Restructure & Cleanup

  **What to do**:
  - Create directories: `client/css`, `client/js`, `client/img`, `server/tests`.
  - Move `SSIMS.html` → `client/index.html`.
  - Move `login.html` → `client/search.html`.
  - Move contents of `css/` → `client/css/`, `img/` → `client/img/`.
  - Create `.gitignore` (ignoring `__pycache__`, `*.db`, `venv`, `.sisyphus`).
  - **Do NOT** update internal HTML paths yet (will be done in respective frontend tasks).

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`bash`]

  **QA Scenarios**:
  ```
  Scenario: Verify directory structure
    Tool: bash
    Steps:
      1. ls -R client server
    Expected Result: Client has css/js/img/index.html/search.html. Server exists.
    Evidence: .sisyphus/evidence/task-1-structure.txt
  ```

- [x] 2. Python Environment Setup
- [x] 3. App Scaffold & Test Infrastructure

  **What to do**:
  - Create `server/main.py` with a basic `app = FastAPI()`.
  - Create `server/tests/__init__.py`.
  - Create `server/tests/conftest.py`.
  - Define `session` fixture using `StaticPool` and in-memory SQLite (`sqlite:///:memory:`).
  - Define `client` fixture using `TestClient(app)`.

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`python`]

  **References**:
  - FastAPI Testing: `https://fastapi.tiangolo.com/tutorial/testing/`

  **QA Scenarios**:
  ```
  Scenario: Verify test setup
    Tool: bash
    Steps:
      1. Create a dummy test file `server/tests/test_sanity.py`
      2. python3 -m pytest server/tests/test_sanity.py
    Expected Result: 1 passed
    Evidence: .sisyphus/evidence/task-3-pytest.txt
  ```

- [x] 4. Database & Models Implementation

  **What to do**:
  - Create `server/database.py`: `engine` setup (sync), `create_db_and_tables`.
  - Create `server/models.py`:
    - `Course` SQLModel: `id`, `name`.
    - `CompanyCourseLink` SQLModel (junction): `company_id`, `course_id`.
    - `Company` SQLModel: `id`, `name`, `description`, `location`, `slots_available`, `email`, `status`.
    - Add `courses` relationship to `Company` (Many-to-Many via Link).
  - Create `server/tests/test_models.py`: Test creating linked Companies and Courses.

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`python`]

  **QA Scenarios**:
  ```
  Scenario: Run model tests
    Tool: bash
    Steps:
      1. python3 -m pytest server/tests/test_models.py
    Expected Result: All tests pass
    Evidence: .sisyphus/evidence/task-4-models.txt
  ```

- [x] 5. Seed Data & Script

  **What to do**:
  - Create `data.json`:
    - `courses`: List of course names.
    - `companies`: Array of objects (with `course_names` list to link).
  - Create `server/seed.py`:
    - Seed `Course` table first (get or create).
    - Seed `Company` table.
    - Create `CompanyCourseLink` entries to link them.
  - Create `server/tests/test_seed.py`: Test that seeding populates tables and relationships.

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`python`]

  **QA Scenarios**:
  ```
  Scenario: Run seed tests
    Tool: bash
    Steps:
      1. python3 -m pytest server/tests/test_seed.py
    Expected Result: All tests pass (DB populated with relationships)
    Evidence: .sisyphus/evidence/task-5-seed.txt
  ```

- [x] 6. API Endpoints Implementation

  **What to do**:
  - Create `server/api.py` (or `server/routes.py`).
  - Implement `GET /api/companies`:
    - Query params: `location` (str, optional), `course` (str, optional).
    - Filter by `Company.location` (case-insensitive).
    - Filter by `Company.courses` relationship (if course param provided).
  - Implement `GET /api/companies/{id}`.
    - Include course list in response.
  - Create `server/tests/test_api.py`: Test filtering by course relationship.

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`python`]

  **QA Scenarios**:
  ```
  Scenario: Run API tests
    Tool: bash
    Steps:
      1. python3 -m pytest server/tests/test_api.py
    Expected Result: All tests pass (200 OK for valid, 404 for invalid)
    Evidence: .sisyphus/evidence/task-6-api.txt
  ```

- [x] 7. FastAPI App & Static Serving

  **What to do**:
  - Create `server/main.py`.
  - Setup `lifespan` to call `create_db_and_tables` and `seed_data`.
  - Include API router with prefix `/api`.
  - Mount `client/` as StaticFiles at `/static`.
  - Add route `GET /` returning `client/index.html`.
  - **Note**: Ensure API routes are registered BEFORE static mount.

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`python`]

  **QA Scenarios**:
  ```
  Scenario: Verify server startup and serving
    Tool: bash
    Steps:
      1. uvicorn server.main:app --host 0.0.0.0 --port 8000 &
      2. sleep 5
      3. curl -v http://localhost:8000/api/companies
      4. curl -v http://localhost:8000/
      5. kill %1
    Expected Result: 200 OK for both API and Root
    Evidence: .sisyphus/evidence/task-7-server.txt
  ```

- [x] 8. Landing Page (index.html) Migration

  **What to do**:
  - Update `client/index.html` (formerly SSIMS.html).
  - Fix CSS links: `css/SSIMS.css` → `/static/css/SSIMS.css`.
  - Fix Image links: `img/...` → `/static/img/...`.
  - Fix JS links.
  - Update "Login" and "Get Started" links to point to `search.html` (via `/static/search.html` or logic).
  - **Constraint**: Do not change visual design.
  - **Safe Implementation**: Use Python for file modification to avoid macOS `sed` issues.
    - `python3 -c "import sys; p='client/index.html'; c=open(p).read(); c=c.replace('css/','/static/css/').replace('img/','/static/img/').replace('js/','/static/js/'); open(p,'w').write(c)"`

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`python`]

  **QA Scenarios**:
  ```
  Scenario: Verify landing page assets
    Tool: bash
    Steps:
      1. Start server
      2. curl http://localhost:8000/ | grep "/static/css"
    Expected Result: grep finds updated paths
    Evidence: .sisyphus/evidence/task-8-landing.txt
  ```

- [x] 9. Search Page (login.html refactor)

  **What to do**:
  - Update `client/search.html` (formerly login.html).
  - Update asset paths (CSS/Images) - **Use Python for replacement**.
  - **Form Update**:
    - Remove First Name / Last Name inputs.
    - Change "Course of Study" input to `<select>` with options (Computer Engineering, etc.).
    - Ensure "Preferred Location" is `<select>` (Lagos, Abuja, PH).
  - **Logic**:
    - Add JS to intercept submit.
    - Construct URL params `?course=X&location=Y`.
    - Redirect to `results.html`.

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: [`frontend-ui-ux`]

  **QA Scenarios**:
  ```
  Scenario: Verify search form elements
    Tool: playwright
    Steps:
      1. Open /static/search.html
      2. Assert "First Name" input is NOT visible
      3. Assert "Course of Study" is a SELECT
      4. Assert "Preferred Location" is a SELECT
    Expected Result: Pass
    Evidence: .sisyphus/evidence/task-9-search.png
  ```

- [x] 10. Results Page Implementation

  **What to do**:
  - Create `client/results.html`.
  - **UI**: Copy header/footer/style from `search.html`.
  - **Logic (`client/js/results.js`)**:
    - Parse URL params.
    - `fetch('/api/companies?course=...&location=...')`.
    - Render list of company cards.
    - Handle "No results found".
    - Link cards to `details.html?id=ID`.

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: [`frontend-ui-ux`]

  **QA Scenarios**:
  ```
  Scenario: Verify results fetching
    Tool: playwright
    Steps:
      1. Start server with seed data
      2. Go to /static/results.html?location=Lagos
      3. Wait for fetch
      4. Assert company cards > 0
    Expected Result: Companies displayed
    Evidence: .sisyphus/evidence/task-10-results.png
  ```

- [x] 11. Details Page Implementation

  **What to do**:
  - Create `client/details.html`.
  - **Logic (`client/js/details.js`)**:
    - Parse `?id=ID`.
    - `fetch('/api/companies/ID')`.
    - Display full company info (Description, Requirements, Email).
    - Add "Apply Now" button (`mailto:email`).
    - Add "Back to Results" button.

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: [`frontend-ui-ux`]

  **QA Scenarios**:
  ```
  Scenario: Verify details fetching
    Tool: playwright
    Steps:
      1. Start server
      2. Go to /static/details.html?id=1
      3. Assert Company Name is visible
      4. Assert Email is visible
    Expected Result: Correct data shown
    Evidence: .sisyphus/evidence/task-11-details.png
  ```

- [x] 12. End-to-End Integration Test

  **What to do**:
  - Create a Playwright test script `e2e_test.py`.
  - Flow: Home -> Click Get Started -> Select Filters -> Search -> Click Result -> View Details.
  - Run verifying the full user journey.

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`python`, `playwright`]

  **QA Scenarios**:
  ```
  Scenario: Full user journey
    Tool: bash
    Steps:
      1. python3 e2e_test.py
    Expected Result: Test passes
    Evidence: .sisyphus/evidence/task-12-e2e.txt
  ```

- [x] 13. Final Code Quality & Cleanup

  **What to do**:
  - Run `flake8` or `black` on server code.
  - Ensure all comments are clear.
  - Delete any temporary test files (if any).
  - Verify `README.md` instructions (optional update).

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`

  **QA Scenarios**:
  ```
  Scenario: Lint check
    Tool: bash
    Steps:
      1. pip install black
      2. black --check server/
    Expected Result: Pass
    Evidence: .sisyphus/evidence/task-13-quality.txt
  ```

---

## Final Verification Wave (MANDATORY)

- [x] F1. **Plan Compliance Audit** — `oracle`
  
  **QA Scenarios**:
  ```
  Scenario: Check critical files exist
    Tool: bash
    Steps:
      1. ls client/search.html server/models.py data.json
    Expected Result: All files listed
    Evidence: .sisyphus/evidence/f1-files.txt
  ```

- [x] F2. **Code Quality Review** — `unspecified-high`
  
  **QA Scenarios**:
  ```
  Scenario: Check for secrets and errors
    Tool: bash
    Steps:
      1. grep -r "api_key" server/ || true
      2. grep -r "TODO" server/ || true
    Expected Result: No critical secrets or blocking TODOs found
    Evidence: .sisyphus/evidence/f2-quality.txt
  ```

- [x] F3. **Real Manual QA Simulation** — `unspecified-high`
  
  **QA Scenarios**:
  ```
  Scenario: Simulate user search flow
    Tool: playwright
    Steps:
      1. Start server (uvicorn)
      2. Navigate to /
      3. Click "Get Started"
      4. Select "Lagos"
      5. Submit
      6. Assert URL contains "?location=Lagos"
    Expected Result: Navigation and URL update correct
    Evidence: .sisyphus/evidence/f3-manual.png
  ```

- [x] F4. **Scope Fidelity Check** — `deep`
  
  **QA Scenarios**:
  ```
  Scenario: Verify NO auth endpoints
    Tool: bash
    Steps:
      1. grep -r "login" server/api.py || true
      2. grep -r "password" server/models.py || true
    Expected Result: No auth logic found (except search.html filename references)
    Evidence: .sisyphus/evidence/f4-scope.txt
  ```

---

## Success Criteria

### Verification Commands
```bash
# Backend Tests
python3 -m pytest server/tests/

# Server Run
uvicorn server.main:app --reload

# E2E
python3 e2e_test.py
```

### Final Checklist
- [ ] Project structure is `client/` and `server/`.
- [ ] `login.html` is now a Search Filter.
- [ ] Database seeds automatically on startup.
- [ ] Frontend fetches data from API.
