from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.parent

TEST_DB_PATH = BASE_DIR / 'testing.db'

TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"

os.environ.setdefault('DATABASE_URL', str(TEST_DB_URL))

from fastapi.testclient import TestClient
from ..main import app


client = TestClient(app)


def clean_testing():
    if TEST_DB_PATH.exists():
        os.remove(TEST_DB_PATH)
