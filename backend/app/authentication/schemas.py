from enum import Enum

from pydantic import BaseModel, EmailStr, validator


class CurrenciesEnum(str, Enum):
    rubles = '₽'
    dollars = '$'


class UserOut(BaseModel):
    email: EmailStr
    currency: CurrenciesEnum

    class Config:
        orm_mode = True


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class LoginData(BaseModel):
    email: EmailStr
    password: str


class RegistrationData(BaseModel):
    email: EmailStr
    password1: str
    password2: str
    currency: CurrenciesEnum

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')

        return v
