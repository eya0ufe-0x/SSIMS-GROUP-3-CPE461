from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from sqlmodel import Session
from server.database import create_db_and_tables
from server.seed import seed_data
from server.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    # Create a new session for seeding
    # We create a new session because get_session yields a session
    # but we need a session object here.
    # Alternatively, we can use dependency injection if we refactor seeding.
    # For simplicity, we create a session manually.
    from server.database import engine

    with Session(engine) as session:
        seed_data(session)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api")

# Mount static files
app.mount("/static", StaticFiles(directory="client"), name="static")


@app.get("/")
async def read_root():
    from fastapi.responses import FileResponse

    return FileResponse("client/index.html")
