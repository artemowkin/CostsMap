import sqlalchemy

from .main import metadata, engine


categories = sqlalchemy.Table("categories", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "title", sqlalchemy.String(50), unique=True, nullable=False
    ),
    sqlalchemy.Column("costs_limit", sqlalchemy.Integer),
    sqlalchemy.Column("color", sqlalchemy.String(10), nullable=False),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id", ondelete="CASCADE")
    ),

    sqlalchemy.CheckConstraint('costs_limit >= 0'),
)

metadata.create_all(engine)
