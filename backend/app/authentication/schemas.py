from enum import Enum

from pydantic import BaseModel, EmailStr


class CurrenciesEnum(str, Enum):
    rubles = '₽'
    dollars = '$'


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class LoginData(BaseModel):
    email: EmailStr
    password: str
    currency: CurrenciesEnum
