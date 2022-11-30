from sqlalchemy import MetaData, create_engine
from databases import Database

from .settings import config


engine = create_engine(config.database_url)

metadata = MetaData()


database = Database(config.database_url)
