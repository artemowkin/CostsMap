from datetime import datetime
import calendar

from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import BaseModel

from ..db.accounts import users
from ..schemas.accounts import UserRegistration, Token, UserLogIn, UserIn
from ..settings import config


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
            await func(*args, **kwargs)
        except (UniqueViolationError, IntegrityError):
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )

    return inner


@user_exists_decorator
async def create_user_in_db(user: UserRegistration):
    """Create entry in db for user"""
    hashed_user_password = hash_password(user.password1)
    creation_data = UserInDb(**user.dict(), password=hashed_user_password)
    creation_query = users.insert().values(**creation_data.dict())
    await config.database.execute(creation_query)


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


def decode_token(token: str):
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


async def check_user_password(user: UserLogIn):
    """Get user from db and check do passwords match"""
    db_user = await get_user_by_email(user.email)
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")


async def get_user_by_email(user_email: str):
    """Get user from DB using email"""
    get_query = users.select().where(users.c.email == user_email)
    db_user = await config.database.fetch_one(get_query)
    if not db_user: raise HTTPException(
        status_code=400, detail="User with this email doesn't exist"
    )

    return db_user


@user_exists_decorator
async def update_user_data(email: str, changing_data: UserIn):
    """Update the user information"""
    update_query = users.update().values(**changing_data.dict()).where(
        users.c.email == email
    )
    result = await config.database.execute(update_query)
    return result


async def update_user_password(email: str, new_password: str):
    """Update password for user"""
    password_hash = hash_password(new_password)
    update_query = users.update().values(password=password_hash).where(
        users.c.email == email
    )
    await config.database.execute(update_query)
