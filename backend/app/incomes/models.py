from uuid import uuid4
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID, Numeric
from sqlalchemy import func

from ..authentication.models import User
from ..cards.models import Card
from ..project.db import Base


class Income(Base):
    __tablename__ = 'incomes'

    uuid = mapped_column(UUID, primary_key=True, default=uuid4)
    amount = mapped_column(Numeric(precision=12, scale=2))
    date: Mapped[datetime.date] = mapped_column(server_default=func.current_date())
    card_id: Mapped[str] = mapped_column(ForeignKey(Card.uuid))
    card: Mapped[Card] = relationship(back_populates='incomes')
    owner_id: Mapped[str] = mapped_column(ForeignKey(User.uuid))
    owner: Mapped[User] = relationship()
    pub_datetime: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
