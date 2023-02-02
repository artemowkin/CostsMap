from uuid import uuid4
import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import Numeric, UUID

from ..authentication.models import User
from ..cards.models import Card
from ..project.db import Base


class Income(Base):
    __tablename__ = 'incomes'

    uuid = mapped_column(UUID, primary_key=True, default=uuid4)
    amount = mapped_column(Numeric(precision=12, scale=2))
    date: Mapped[datetime.date] = mapped_column(server_default=func.now())
    card_id: Mapped[str] = mapped_column(ForeignKey(Card.uuid, ondelete='CASCADE'))
    owner_id: Mapped[str] = mapped_column(ForeignKey(User.uuid, ondelete='CASCADE'))
    pub_datetime: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    card: Mapped[Card] = relationship(back_populates='incomes')
    owner: Mapped[User] = relationship()
