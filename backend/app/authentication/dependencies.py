from fastapi import Security, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from .services import AuthStore, oauth2_scheme
from .models import User
from ..project.settings import settings
from ..project.dependencies import use_session


def use_auth_store(session: AsyncSession = Depends(use_session)) -> AuthStore:
    """Returns initialized auth store with secret key from project settings"""
    return AuthStore(settings.secret_key, session)


def use_token(credentials: HTTPAuthorizationCredentials = Security(oauth2_scheme)) -> str:
    """Returns token from request"""
    return credentials.credentials


async def auth_required(token: str = Depends(use_token), auth_store: AuthStore = Depends(use_auth_store)) -> User:
    """Returns user instance from request token"""
    user = await auth_store.get_user_from_access_token(token)
    return user
