from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID, Numeric, String

from ..authentication.models import User
from ..project.db import Base


class Card(Base):
    __tablename__ = 'cards'

    uuid = mapped_column(UUID, primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(length=50), unique=True)
    currency: Mapped[str] = mapped_column(String(length=1))
    color: Mapped[str] = mapped_column(String(length=8))
    amount = mapped_column(Numeric(precision=12, scale=2), server_default='0')
    owner_id: Mapped[str] = mapped_column(ForeignKey(User.uuid, ondelete='CASCADE'))
    owner: Mapped[User] = relationship()
    costs = relationship('Cost', back_populates='card')
    incomes = relationship('Income', back_populates='card')
