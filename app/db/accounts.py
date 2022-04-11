import sqlalchemy

from .main import metadata


users = sqlalchemy.Table(
    'users', metadata,

    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        'email', sqlalchemy.String(100), nullable=False, unique=True
    ),
    sqlalchemy.Column('password', sqlalchemy.String(128), nullable=False),
)
