from uuid import uuid4

import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from .main import metadata


users = sqlalchemy.Table("users", metadata,
    sqlalchemy.Column(
        "id", UUID(as_uuid=True), primary_key=True, default=uuid4,
    ),
    sqlalchemy.Column(
        "email", sqlalchemy.String(100), unique=True, nullable=False
    ),
    sqlalchemy.Column("password", sqlalchemy.String(500), nullable=False),
    sqlalchemy.Column("currency", sqlalchemy.String(10), nullable=False),
    sqlalchemy.Column("language", sqlalchemy.String(20), nullable=False),
)
