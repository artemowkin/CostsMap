from ormar import ModelMeta

from .db import metadata, database


class BaseMeta(ModelMeta):
    metadata = metadata
    database = database
