from pathlib import Path

from pydantic import BaseSettings


BASE_DIR = Path(__file__).parent.parent.parent


class ProjectSettings(BaseSettings):
    database_url: str
    redis_url: str
    secret_key: str

    class Config:
        env_file = BASE_DIR / '.env'


settings = ProjectSettings() # type: ignore
