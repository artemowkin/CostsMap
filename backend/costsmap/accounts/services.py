from typing import Mapping, Literal, Any
from datetime import datetime
import calendar

from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import BaseModel

from .models import Users, UserNamedTuple
from .schemas import UserRegistration, Token, UserLogIn, UserIn
from ..project.settings import config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserInDb(BaseModel):
    """Model with data to create user in db"""

    email: str
    password: str
    currency: str
    language: str


def hash_password(password: str) -> str:
    """Return hash for user password"""
    return pwd_context.hash(password)


def user_exists_decorator(func):
    """Handle UniqueViolation when create a new user"""

    async def inner(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (UniqueViolationError, IntegrityError):
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )

    return inner


@user_exists_decorator
async def create_user_in_db(user: UserRegistration) -> UserNamedTuple:
    """Create entry in db for user"""
    hashed_user_password = hash_password(user.password1)
    creation_data = UserInDb(**user.dict(), password=hashed_user_password)
    created_user = await Users.objects.create(**creation_data.dict())
    return created_user


def create_token_for_user(user_email: str,
        exp_date: int | None = None) -> Token:
    """Create JWT token for user"""
    utc_now_timestamp = calendar.timegm(datetime.utcnow().utctimetuple())
    if not exp_date:
        exp_date = utc_now_timestamp + config.jwt_token_exp_delta
    else:
        assert utc_now_timestamp < exp_date

    token_data = {'sub': user_email, 'exp': exp_date}
    jwt_token = jwt.encode(
        token_data, config.secret_key, algorithm=config.jwt_algorithm
    )
    return Token(token=jwt_token, exptime=exp_date)


def decode_token(token: str) -> Mapping[Literal['sub'] | Literal['exp'], Any]:
    """Decode user token and return JSON data from it"""
    unauthenticated_error = HTTPException(
        status_code=401, detail="Token is incorrect",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        decoded_token = jwt.decode(
            token, config.secret_key, algorithms=[config.jwt_algorithm]
        )
        if not 'sub' in decoded_token or not 'exp' in decoded_token:
            raise unauthenticated_error

        utc_now_timestamp = calendar.timegm(datetime.utcnow().utctimetuple())
        if decoded_token['exp'] < utc_now_timestamp:
            raise unauthenticated_error
    except JWTError:
        raise unauthenticated_error

    return decoded_token


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def check_user_password(user: UserLogIn) -> None:
    """Get user from db and check do passwords match"""
    db_user = await Users.objects.get(email=user.email)
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")


async def get_user_by_email(user_email: str) -> UserNamedTuple:
    """Get user from DB using email"""
    db_user = await Users.objects.get(email=user_email)
    if not db_user:
        raise HTTPException(status_code=400, detail="User with this email doesn't exist")

    return db_user


@user_exists_decorator
async def update_user_data(user_id: int, changing_data: UserIn) -> None:
    """Update the user information"""
    await Users.objects.filter(id=user_id).update(**changing_data.dict())


async def update_user_password(email: str, new_password: str) -> None:
    """Update password for user"""
    password_hash = hash_password(new_password)
    await Users.objects.filter(email=email).update(password=password_hash)
