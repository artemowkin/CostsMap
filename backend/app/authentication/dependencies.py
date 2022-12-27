from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials

from .services import AuthStore, oauth2_scheme
from ..project.settings import settings


def use_auth_store() -> AuthStore:
    return AuthStore(settings.secret_key)


def use_token(credentials: HTTPAuthorizationCredentials = Security(oauth2_scheme)) -> str:
    return credentials.credentials
