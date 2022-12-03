from uuid import UUID
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, validator


class Currencies(str, Enum):
    rubles = '₽'
    dollars = '$'


class Languages(str, Enum):
    russian = 'russian'
    english = 'english'


class UserRegistration(BaseModel):
    username: str
    password1: str
    password2: str
    currency: Currencies = Currencies.dollars
    language: Languages = Languages.english

    @validator('password2')
    def check_passwords_match(cls, value, values, **kwargs):
        if 'password1' in values and value in value != values['password1']:
            raise ValueError('passwords do not match')

        return value


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    user_id: str
    exp: datetime | None = None


class UserOut(BaseModel):
    uuid: UUID
    username: str
    currency: Currencies
    language: Languages

    class Config:
        orm_mode = True


class User(UserOut):
    password: str

    class Config:
        orm_mode = True
