from sqlalchemy import MetaData
from async_lru import alru_cache
from databases import Database

from .settings import config


metadata = MetaData()


@alru_cache
async def get_database() -> Database:
    """Dependency that returns database connection"""
    database = Database(config.database_url)
    await database.connect()
    return database
