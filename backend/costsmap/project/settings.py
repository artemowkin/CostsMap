from pathlib import Path

from pydantic import BaseSettings


BASE_DIR = Path(__file__).parent.parent


class Config(BaseSettings):
    database_url: str
    secret_key: str
    jwt_algorithm: str = 'HS256'
    jwt_token_exp_delta = 30 * 24 * 60 * 60 # 30 days
    testing: bool = False

    class Config:
        env_file = BASE_DIR / '.env'


config = Config()
