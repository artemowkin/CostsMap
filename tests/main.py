import os

from app.settings import config


def setup_testing():
    config.is_testing = True


def clean_testing():
    os.remove(config.test_db_path)
