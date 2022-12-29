from decimal import Decimal

from pydantic import BaseModel, Field

from ..authentication.schemas import CurrenciesEnum


class CardIn(BaseModel):
    title: str
    currency: CurrenciesEnum = CurrenciesEnum.dollars
    color: str = Field(..., regex=r"^#[a-fA-F0-9]{6}$")
    amount: Decimal
