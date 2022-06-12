import sqlalchemy
from sqlalchemy.sql import func

from project.db import metadata
from accounts.db import users
from categories.db import categories
from cards.db import cards


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
        "card_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(cards.c.id, ondelete="CASCADE")
    ),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(users.c.id, ondelete="CASCADE")
    ),

    sqlalchemy.CheckConstraint('amount >= 0'),
)
