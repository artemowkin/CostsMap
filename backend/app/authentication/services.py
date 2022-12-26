from datetime import timedelta, datetime

from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import HTTPBearer

from .schemas import LoginData, TokenPair


ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = HTTPBearer()


class JWTManager:

    def __init__(self, secret_key: str, algorithm: str = 'HS256'):
        self._secret = secret_key
        self._alg = algorithm

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, self._secret, algorithm=self._alg)
        return encoded_jwt


class AuthStore:

    def __init__(self, secret_key: str):
        self._jwt = JWTManager(secret_key)

    async def login(self, login_data: LoginData) -> TokenPair:
        pass
