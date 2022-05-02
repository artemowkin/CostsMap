import sqlalchemy

from .main import metadata, get_engine
from .accounts import users


engine = get_engine()


cards = sqlalchemy.Table("cards", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "title", sqlalchemy.String(50), unique=True, nullable=False
    ),
    sqlalchemy.Column("currency", sqlalchemy.String(1), nullable=False),
    sqlalchemy.Column("color", sqlalchemy.String(10), nullable=False),
    sqlalchemy.Column("amount", sqlalchemy.Numeric(9, 2), server_default='0'),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(users.c.id, ondelete="CASCADE")
    ),
)

metadata.create_all(engine)
