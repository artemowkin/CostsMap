from orm import ModelRegistry
from databases import Database

from .settings import config


database = Database(config.database_url)

models = ModelRegistry(database=database)


async def connect_db():
    await database.connect()
