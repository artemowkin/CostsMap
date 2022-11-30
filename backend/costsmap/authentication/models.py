from sqlalchemy import Table, Column, String, ForeignKey

from ..project.databases import metadata


users = Table(
    'users', metadata,

    Column('uuid', String(36), primary_key=True),
    Column('username', String(500), nullable=False, unique=True),
    Column('password', String(500), nullable=False),
)

sessions = Table(
    'sessions', metadata,

    Column('refresh_token', String(500), primary_key=True),
    Column('user_id', String(36), ForeignKey(users.c.uuid)),
)