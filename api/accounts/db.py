import sqlalchemy

from project.db import metadata


users = sqlalchemy.Table("users", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "email", sqlalchemy.String(100), unique=True, nullable=False
    ),
    sqlalchemy.Column("password", sqlalchemy.String(500), nullable=False),
    sqlalchemy.Column("currency", sqlalchemy.String(10), nullable=False),
    sqlalchemy.Column("language", sqlalchemy.String(20), nullable=False),
)
