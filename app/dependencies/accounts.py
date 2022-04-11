from datetime import datetime, timedelta
import os

from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt
from asyncpg.exceptions import UniqueViolationError

from app.schemas.accounts import LoginAuthData, RegistrationAuthData
from app.db.accounts import users
from app.db.main import database


SECRET_KEY = os.getenv('COSTSMAP_SECRET_KEY')

EXPIRES_DATE = 30 * 24 * 60 * 60 # 30 days

ALGORITHM = 'HS256'

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(auth_data: LoginAuthData):
    """Authenticate user using data from request"""
    user = await get_user_by_email(auth_data.email)
    verify_password(auth_data.password, user.password)
    access_token = create_access_token({'sub': user.email})
    return access_token


async def get_user_by_email(email: str):
    """Get user from DB using email field value"""
    select_query = users.select().where(users.c.email == email)
    db_user = await database.fetch_one(select_query)
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect email")

    return db_user


def verify_password(plain_password: str, hashed_password: str):
    """
    Compares plain password from request with hashed password from DB
    """
    print(hashed_password)
    verified = pwd_context.verify(plain_password, hashed_password)
    if not verified:
        raise HTTPException(status_code=401, detail="Incorrect password")


def create_access_token(data: dict, expdate: int = EXPIRES_DATE):
    """Create JWT access token with data and expires date"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expdate)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def registrate_user(auth_data: RegistrationAuthData):
    """Registrate user and create JWT token"""
    create_user_data = get_create_user_data(auth_data)
    await create_user(create_user_data)
    jwt_payload = {'sub': auth_data.email}
    jwt_token = create_access_token(jwt_payload)
    return jwt_token


def get_create_user_data(auth_data: RegistrationAuthData):
    """
    Return a dict with username and hashed password to save it in DB
    """
    hashed_password = pwd_context.hash(auth_data.password1)
    return {'email': auth_data.email, 'password': hashed_password}


async def create_user(create_data: dict):
    """Create user entry in DB"""
    create_query = users.insert().values(**create_data)
    try:
        created_user_id = await database.execute(create_query)
    except UniqueViolationError:
        raise HTTPException(
            status_code=401, detail="User with this email already exists"
        )

    if not created_user_id:
        raise HTTPException(status_code=401, detail="User was not created")

    return created_user_id
