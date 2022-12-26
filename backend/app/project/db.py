from sqlalchemy import create_engine, MetaData
from databases import Database

from .settings import settings


engine = create_engine(settings.database_url)

metadata = MetaData(engine)

database = Database(settings.database_url)
