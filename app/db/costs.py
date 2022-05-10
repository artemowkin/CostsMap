import sqlalchemy
from sqlalchemy.sql import func

from .main import metadata, get_engine
from .accounts import users
from .categories import categories


engine = get_engine()


costs = sqlalchemy.Table("costs", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("amount", sqlalchemy.Numeric(9, 2), nullable=False),
    sqlalchemy.Column("date", sqlalchemy.Date, server_default=func.now()),
    sqlalchemy.Column(
        "category_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(categories.c.id, ondelete="CASCADE")
    ),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(users.c.id, ondelete="CASCADE")
    ),

    sqlalchemy.CheckConstraint('amount >= 0'),
)

metadata.create_all(engine)
