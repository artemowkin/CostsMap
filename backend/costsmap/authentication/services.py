from datetime import datetime, timedelta

import pytz
from fastapi import HTTPException, status
from uuid import uuid4
from sqlalchemy import Table
from passlib.context import CryptContext
from asyncpg.exceptions import UniqueViolationError
from jose import JWTError, jwt

from ..project.databases import database
from ..project.settings import config
from .models import users, sessions
from .schemas import UserRegistration, Token, TokenData, UserLogin, UserOut


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class TokenManager:

    session_table: Table = sessions

    def __init__(
            self, access_token_expdelta_seconds: int,
            refresh_token_expdelta_seconds: int,
            algorithm: str = 'HS256'):
        self._token_data_schema = TokenData
        self._access_token_expdelta = timedelta(seconds=access_token_expdelta_seconds)
        self._refresh_token_expdelta = timedelta(seconds=refresh_token_expdelta_seconds)
        self._algorithm = algorithm

    def _create_token(self, data: TokenData, expire: datetime) -> str:
        encoding_data = data.dict()
        encoding_data['exp'] = expire
        encoded_token = jwt.encode(encoding_data, config.secret_key, algorithm=self._algorithm)
        return encoded_token

    def create_access_token(self, data: TokenData) -> str:
        expire = datetime.utcnow() + self._access_token_expdelta
        return self._create_token(data, expire)

    async def _clear_user_sessions(self, data: TokenData):
        query = self.session_table.delete().where(self.session_table.c.user_id == data.user_id)
        await database.execute(query)

    async def _save_session(self, token: str, user_id: str):
        query = self.session_table.insert().values(refresh_token=token, user_id=user_id)
        await database.execute(query)

    async def create_refresh_token(self, data: TokenData, *, delete_old: bool = True) -> str:
        if delete_old: await self._clear_user_sessions(data)
        expire = datetime.utcnow() + self._refresh_token_expdelta
        refresh_token = self._create_token(data, expire)
        await self._save_session(refresh_token, data.user_id)
        return refresh_token

    def check_token_expired(self, token: str):
        token_data = self.get_token_data(token)
        assert token_data.exp, "Invalid token from db: required exp field"
        if pytz.utc.localize(datetime.utcnow()) >= token_data.exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired'
            )

    def get_token_data(self, token: str) -> TokenData:
        try:
            token_payload = jwt.decode(token, config.secret_key, algorithms=[self._algorithm])
            token_data = self._token_data_schema(**token_payload)
            return token_data
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect token'
            )


class Authentication:

    table: Table = users

    def __init__(self) -> None:
        self._token_manager = TokenManager(
            access_token_expdelta_seconds=24*60*60, # 1 day
            refresh_token_expdelta_seconds=30*24*60*60 # 30 days
        )

    async def _create_token_pair(self, user_id: str) -> Token:
        token_data = TokenData(user_id=user_id)
        access_token = self._token_manager.create_access_token(token_data)
        refresh_token = await self._token_manager.create_refresh_token(token_data)
        return Token(access_token=access_token, refresh_token=refresh_token)

    async def registrate(self, user_data: UserRegistration) -> Token:
        uuid = str(uuid4())
        hashed_password = pwd_context.hash(user_data.password1)
        query = self.table.insert().values(uuid=uuid, username=user_data.username, password=hashed_password)
        try:
            await database.execute(query)
            token = await self._create_token_pair(uuid)
            return token
        except UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exists"
            )

    async def _get_user_by_username(self, username: str):
        query = self.table.select().where(self.table.c.username == username)
        user = await database.fetch_one(query)
        return user

    async def login(self, user_data: UserLogin) -> Token:
        user = await self._get_user_by_username(user_data.username)
        if not user or not pwd_context.verify(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        token = await self._create_token_pair(user.uuid)
        return token

    async def get_user_by_token(self, token: str) -> UserOut:
        self._token_manager.check_token_expired(token)
        token_data = self._token_manager.get_token_data(token)
        query = self.table.select().where(self.table.c.uuid == token_data.user_id)
        user = await database.fetch_one(query)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect token"
            )

        return UserOut.from_orm(user)

    async def refresh_tokens(self, refresh_token: str) -> Token:
        self._token_manager.check_token_expired(refresh_token)
        token_data = self._token_manager.get_token_data(refresh_token)
        new_access_token = self._token_manager.create_access_token(token_data)
        return Token(access_token=new_access_token, refresh_token=refresh_token)
