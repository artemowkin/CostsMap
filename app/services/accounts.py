from datetime import datetime
import calendar

from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError
from passlib.context import CryptContext
from jose import jwt
from pydantic import BaseModel

from ..db.main import database
from ..db.accounts import users
from ..schemas.accounts import UserRegistration, Token
from ..settings import JWT_TOKEN_EXP_DELTA, SECRET_KEY, JWT_ALGORITHM


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
        except UniqueViolationError:
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
    await database.execute(creation_query)


def create_token_for_user(user_email: str,
        exp_date: int | None = None) -> Token:
    """Create JWT token for user"""
    if not exp_date:
        utc_now_timestamp = calendar.timegm(datetime.utcnow().utctimetuple())
        exp_date = utc_now_timestamp + JWT_TOKEN_EXP_DELTA

    token_data = {'sub': user_email, 'exp': exp_date}
    jwt_token = jwt.encode(token_data, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return Token(token=jwt_token, exptime=exp_date)
