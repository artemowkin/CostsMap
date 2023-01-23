from fastapi import Security, Depends
from fastapi.security import HTTPAuthorizationCredentials

from .services import AuthStore, oauth2_scheme
from .models import User
from ..project.settings import settings


def use_auth_store() -> AuthStore:
    """Returns initialized auth store with secret key from project settings"""
    return AuthStore(settings.secret_key)


def use_token(credentials: HTTPAuthorizationCredentials = Security(oauth2_scheme)) -> str:
    """Returns token from request"""
    return credentials.credentials


async def auth_required(token: str = Depends(use_token), auth_store: AuthStore = Depends(use_auth_store)) -> User:
    """Returns user instance from request token"""
    user = await auth_store.get_user_from_access_token(token)
    return user
