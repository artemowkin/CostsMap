import os
from pathlib import Path

from databases import Database


def get_env(env_name: str, default_value: str | None = None):
    """
    Return environment variable value if it exists. Else raise RuntimeError
    """
    env_value = os.getenv(env_name)
    if not env_value:
        if default_value: return default_value
        raise RuntimeError(f"You need to set {env_name} env variable")

    return env_value


class Config:
    """Class with application settings"""

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.test_db_path = self.base_dir / 'testdb.db'
        self.test_db_url = f"sqlite:///{self.test_db_path}"
        self.database_url = get_env('COSTSMAP_DATABASE_URL')
        self.secret_key = get_env('COSTSMAP_SECRET_KEY')
        self.jwt_algorithm = 'HS256'
        self.jwt_token_exp_delta = 30 * 24 * 60 * 60 # 30 days
        self.is_testing = False
        self._database: Database | None = None

    @property
    def database(self):
        assert self._database
        return self._database

    @database.setter
    def database(self, value: Database):
        self._database = value


config = Config()
