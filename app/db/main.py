import databases
from sqlalchemy import create_engine, MetaData

from ..settings import config


metadata = MetaData()


def get_database():
    if config.is_testing:
        return databases.Database(config.test_db_url)

    return databases.Database(config.database_url)


def get_engine():
    if config.is_testing:
        return create_engine(config.test_db_url)

    return create_engine(config.database_url)
