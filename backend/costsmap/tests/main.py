import os

from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from databases import Database

from project.db import get_database
from project.settings import BASE_DIR
from main import app


TEST_DB_PATH = BASE_DIR / 'testing.db'

TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"


@app.on_event("startup")
def clean_startup():
    pass


async def override_get_db():
    database = Database(TEST_DB_URL)
    try:
        await database.connect()
        yield database
    finally:
        await database.disconnect()


app.dependency_overrides[get_database] = override_get_db

client = TestClient(app)


def setup_testing():
    from accounts.db import users
    from categories.db import categories
    from cards.db import cards
    from project.db import metadata
    engine = create_engine(TEST_DB_URL)
    metadata.create_all(engine)


def clean_testing():
    if TEST_DB_PATH.exists():
        os.remove(TEST_DB_PATH)
