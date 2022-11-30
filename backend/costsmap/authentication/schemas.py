from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, validator


class UserRegistration(BaseModel):
    username: str
    password1: str
    password2: str

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

    class Config:
        orm_mode = True


class User(UserOut):
    password: str

    class Config:
        orm_mode = True
