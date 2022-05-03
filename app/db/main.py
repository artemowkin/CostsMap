from fastapi import FastAPI
import databases
from sqlalchemy import create_engine, MetaData

from ..settings import config


metadata = MetaData()


def get_engine():
    if config.is_testing:
        return create_engine(config.test_db_url)

    return create_engine(config.database_url)
