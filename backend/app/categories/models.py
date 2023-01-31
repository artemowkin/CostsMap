from uuid import uuid4

from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID, String

from ..authentication.models import User
from ..project.db import Base


class Category(Base):
    __tablename__ = "categories"

    uuid = mapped_column(UUID, primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(length=50), unique=True)
    costs_limit: Mapped[int] = mapped_column(nullable=False)
    color: Mapped[str] = mapped_column(String(length=8))
    owner_id: Mapped[str] = mapped_column(ForeignKey(User.uuid, ondelete='CASCADE'))
    owner: Mapped[User] = relationship()
    costs = relationship('Cost', back_populates='category')
