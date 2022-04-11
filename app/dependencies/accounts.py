from datetime import datetime, timedelta
import os

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from asyncpg.exceptions import UniqueViolationError

from app.schemas.accounts import LoginAuthData, RegistrationAuthData, User
from app.db.accounts import users
from app.db.main import database


SECRET_KEY = os.getenv('COSTSMAP_SECRET_KEY')

EXPIRES_DATE = 30 * 24 * 60 * 60 # 30 days

ALGORITHM = 'HS256'

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def authenticate_user(auth_data: LoginAuthData) -> str:
    """Authenticate user using data from request"""
    user = await get_user_by_email(auth_data.email)
    verify_password(auth_data.password, user.password)
    access_token = create_access_token({'sub': user.email})
    return access_token


async def get_user_by_email(email: str) -> User:
    """Get user from DB using email field value"""
    select_query = users.select().where(users.c.email == email)
    db_user = await database.fetch_one(select_query)
    if not db_user:
        raise HTTPException(
            status_code=401, detail="Incorrect email",
            headers={'WWW-Authenticate': 'Bearer'}
        )

    user = User.from_orm(db_user)
    return user


def verify_password(plain_password: str, hashed_password: str):
    """
    Compares plain password from request with hashed password from DB
    """
    verified = pwd_context.verify(plain_password, hashed_password)
    if not verified:
        raise HTTPException(
            status_code=401, detail="Incorrect password",
            headers={'WWW-Authenticate': 'Bearer'}
        )


def create_access_token(data: dict, expdate: int = EXPIRES_DATE) -> str:
    """Create JWT access token with data and expires date"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expdate)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def registrate_user(auth_data: RegistrationAuthData) -> str:
    """Registrate user and create JWT token"""
    create_user_data = get_create_user_data(auth_data)
    await create_user(create_user_data)
    jwt_payload = {'sub': auth_data.email}
    jwt_token = create_access_token(jwt_payload)
    return jwt_token


def get_create_user_data(auth_data: RegistrationAuthData) -> dict:
    """
    Return a dict with username and hashed password to save it in DB
    """
    hashed_password = pwd_context.hash(auth_data.password1)
    return {'email': auth_data.email, 'password': hashed_password}


async def create_user(create_data: dict) -> int:
    """Create user entry in DB"""
    create_query = users.insert().values(**create_data)
    try:
        created_user_id = await database.execute(create_query)
    except UniqueViolationError:
        raise HTTPException(
            status_code=401, detail="User with this email already exists",
            headers={'WWW-Authenticate': 'Bearer'}
        )

    if not created_user_id:
        raise HTTPException(
            status_code=401, detail="User was not created",
            headers={'WWW-Authenticate': 'Bearer'}
        )

    return created_user_id


async def current_user(token: str = Depends(oauth)):
    """Return user getted by token"""
    token_payload = _get_jwt_token_payload(token)
    user_email = token_payload['sub']
    user = await get_user_by_email(user_email)
    return user


def _get_jwt_token_payload(token: str):
    """Decode jwt token and return its payload"""
    token_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if not 'sub' in token_payload or not 'exp' in token_payload:
        raise HTTPException(
            status_code=401, detail="incorrect jwt token",
            headers={'WWW-Authenticate': 'Bearer'}
        )
    elif datetime.utcnow().timestamp() > token_payload['exp']:
        raise HTTPException(
            status_code=401, detail="the token expired",
            headers={'WWW-Authenticate': 'Bearer'}
        )

    return token_payload
