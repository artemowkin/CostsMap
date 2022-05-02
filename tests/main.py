import os

from app.settings import config


def setup_testing():
    config.is_testing = True
    from app.db.accounts import users
    from app.db.categories import categories
    from app.db.main import metadata, get_engine
    engine = get_engine()
    metadata.create_all(engine)


def clean_testing():
    os.remove(config.test_db_path)
