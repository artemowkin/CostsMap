from sqlalchemy import Table, Column, String, Numeric

from ..project.databases import metadata


categories = Table(
    'categories', metadata,

    Column('uuid', String(36), primary_key=True),
    Column('title', String(500), unique=True),
    Column('limit', Numeric(16, 2)),
    Column('color', String(7)),
)