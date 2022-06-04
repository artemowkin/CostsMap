import os

from databases import Database

from app.settings import config


def _create_test_db_if_doesnt_exist():
    if not os.path.exists(config.test_db_path):
        os.mknod(config.test_db_path)


def setup_testing():
    _create_test_db_if_doesnt_exist()
    config.is_testing = True
    config.database = Database(config.test_db_url)
    from app.db.accounts import users
    from app.db.categories import categories
    from app.db.main import metadata, get_engine
    engine = get_engine()
    metadata.create_all(engine)


def clean_testing():
    if os.path.exists(config.test_db_path):
        os.remove(config.test_db_path)
