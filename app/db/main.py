import databases
from sqlalchemy import create_engine, MetaData

from ..settings import DATABASE_URL


database = databases.Database(DATABASE_URL)

metadata = MetaData()

engine = create_engine(DATABASE_URL)

metadata.create_all(engine)
