import datetime
from uuid import uuid4

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID, Numeric

from ..authentication.models import User
from ..categories.models import Category
from ..cards.models import Card
from ..project.db import Base


class Cost(Base):
    __tablename__ = 'costs'

    uuid = mapped_column(UUID, primary_key=True, default=uuid4)
    amount = mapped_column(Numeric(precision=12, scale=2))
    date: Mapped[datetime.date] = mapped_column(server_default=func.now())
    card_id: Mapped[str] = mapped_column(ForeignKey(Card.uuid, ondelete='CASCADE'))
    owner_id: Mapped[str] = mapped_column(ForeignKey(User.uuid, ondelete='CASCADE'))
    pub_datetime: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    category_id: Mapped[str] = mapped_column(ForeignKey(Category.uuid, ondelete='CASCADE'))
    category: Mapped[Category] = relationship(back_populates='costs')
    card: Mapped[Card] = relationship(back_populates='costs')
    owner: Mapped[User] = relationship()
