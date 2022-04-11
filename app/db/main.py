import os

import databases
import sqlalchemy


def get_database_url() -> str:
    url = os.getenv('DATABASE_URL', '')
    if not url:
        raise RuntimeError(
            "You need to set up `DATABASE_URL` environment variable"
        )

    return url


DATABASE_URL = get_database_url()

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)
