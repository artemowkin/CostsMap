from datetime import timedelta, datetime

from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import HTTPBearer
from fastapi import HTTPException, status
from asyncpg.exceptions import UniqueViolationError

from .schemas import LoginData, TokenPair, RegistrationData
from .models import User
from ..project.redis import redis_db


ACCESS_TOKEN_EXPIRE_MINUTES = 30

REFRESH_TOKEN_EXPIRE_DAYS = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = HTTPBearer()


def _handle_unique_violation(func):

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except UniqueViolationError:
            raise HTTPException(status.HTTP_409_CONFLICT, "User with this email already exists")

    return wrapper


class JWTManager:

    def __init__(self, secret_key: str, algorithm: str = 'HS256'):
        self._secret = secret_key
        self._alg = algorithm

    def _generate_token(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, self._secret, algorithm=self._alg)
        return encoded_jwt

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        expires_delta = expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = self._generate_token(data, expires_delta)
        return token

    def create_refresh_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        expires_delta = expires_delta if expires_delta else timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        token = self._generate_token(data, expires_delta)
        return token

    def decode_token(self, token: str) -> dict:
        credentials_exception = HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect token")
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._alg])
            if not 'email' in payload or not 'exp' in payload or payload['exp'] <= datetime.utcnow().timestamp():
                raise credentials_exception

            return payload
        except JWTError:
            raise credentials_exception


class DBAuth:

    def __init__(self):
        self._model = User

    async def get_user_by_email(self, email: str) -> User | None:
        user = await self._model.objects.get_or_none(email=email)
        return user

    async def create_user(self, registration_data: RegistrationData, hashed_password: str) -> User:
        user_data = registration_data.dict(exclude={'password1': True, 'password2': True})
        user = await self._model.objects.create(**user_data, password=hashed_password)
        return user


class SessionStorage:

    def __init__(self):
        self._db = redis_db

    async def add(self, email: str, token_pair: TokenPair):
        await self._db.hset(email, token_pair.access_token, token_pair.refresh_token)

    async def delete(self, email: str, token: str):
        await self._db.hdel(email, token)

    async def clear_refresh_token_sessions(self, email: str, token: str):
        sessions = await self._db.hgetall(email)
        access_tokens = [access_token for access_token in sessions if sessions[access_token] == token.encode()]
        if not access_tokens: return
        await self._db.hdel(email, *access_tokens)

    async def check_is_session_active(self, email: str, access_token: str) -> bool:
        refresh_token = await self._db.hget(email, access_token)
        return bool(refresh_token)

    async def check_refresh_token(self, email: str, refresh_token: str) -> bool:
        sessions = await self._db.hgetall(email)
        return refresh_token.encode() in sessions.values()


class AuthStore:

    def __init__(self, secret_key: str):
        self._jwt = JWTManager(secret_key)
        self._db = DBAuth()
        self._session = SessionStorage()

    def _generate_token_pair(self, email) -> TokenPair:
        access_token = self._jwt.create_access_token({'email': email})
        refresh_token = self._jwt.create_refresh_token({'email': email})
        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    async def login(self, login_data: LoginData) -> TokenPair:
        user = await self._db.get_user_by_email(login_data.email)
        if not user or not pwd_context.verify(login_data.password, user.password):
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect email or password")

        token_pair = self._generate_token_pair(login_data.email)
        await self._session.add(login_data.email, token_pair)
        return token_pair

    @_handle_unique_violation
    async def registrate(self, registration_data: RegistrationData) -> TokenPair:
        hashed_password = pwd_context.hash(registration_data.password1)
        db_user = await self._db.create_user(registration_data, hashed_password)
        token_pair = self._generate_token_pair(db_user.email)
        await self._session.add(db_user.email, token_pair)
        return token_pair

    async def _get_user_from_token(self, token: str) -> User:
        payload = self._jwt.decode_token(token)
        db_user = await self._db.get_user_by_email(payload['email'])
        if not db_user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect token")

        return db_user

    async def get_user_from_access_token(self, token: str) -> User:
        db_user = await self._get_user_from_token(token)
        is_session_active = await self._session.check_is_session_active(db_user.email, token)
        if not is_session_active:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect token")

        return db_user

    async def _get_user_from_refresh_token(self, token: str) -> User:
        db_user = await self._get_user_from_token(token)
        is_token_in_session = await self._session.check_refresh_token(db_user.email, token)
        if not is_token_in_session:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect token")

        return db_user

    async def refresh(self, token: str) -> TokenPair:
        db_user = await self._get_user_from_refresh_token(token)
        await self._session.clear_refresh_token_sessions(db_user.email, token)
        access_token = self._jwt.create_access_token({'email': db_user.email})
        token_pair = TokenPair(access_token=access_token, refresh_token=token)
        await self._session.add(db_user.email, token_pair)
        return token_pair

    async def logout(self, token: str) -> None:
        db_user = await self.get_user_from_access_token(token)
        await self._session.delete(db_user.email, token)
