import sqlalchemy

from .main import metadata
from .accounts import users


categories = sqlalchemy.Table(
    'categories', metadata,

    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        'title', sqlalchemy.String(50), nullable=False, unique=True
    ),
    sqlalchemy.Column('owner', sqlalchemy.ForeignKey(
        users.c.id, ondelete="CASCADE"
    )),

    sqlalchemy.UniqueConstraint('title', 'owner'),
)
