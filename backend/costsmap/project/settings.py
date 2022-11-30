from pathlib import Path

from pydantic import BaseSettings


BASE_DIR = Path(__file__).parent.parent


class Config(BaseSettings):
    """Класс конфигурации проекта"""

    database_url: str
    secret_key: str

    class Config:
        env_file = BASE_DIR / '..' / '.env'


config = Config()
