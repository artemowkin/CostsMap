from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from .settings import settings


engine = create_async_engine(settings.database_url)

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    ...
