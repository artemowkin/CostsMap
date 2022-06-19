import sqlalchemy
from sqlalchemy.sql import func

from project.db import metadata
from cards.db import cards
from accounts.db import users


incomes = sqlalchemy.Table("incomes", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_currency_amount", sqlalchemy.Numeric(9, 2), nullable=False),
    sqlalchemy.Column("card_currency_amount", sqlalchemy.Numeric(9, 2), nullable=True),
    sqlalchemy.Column("date", sqlalchemy.Date, server_default=func.now()),
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

    sqlalchemy.CheckConstraint('user_currency_amount >= 0'),
    sqlalchemy.CheckConstraint('card_currency_amount is null or card_currency_amount >= 0')
)
