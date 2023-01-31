from uuid import uuid4

from sqlalchemy.types import UUID, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from ..project.db import Base


class User(Base):
    __tablename__ = 'users'

    uuid = mapped_column(UUID, primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(length=200), unique=True)
    password: Mapped[str] = mapped_column(String(length=500))
    currency: Mapped[str] = mapped_column(String(length=1))
