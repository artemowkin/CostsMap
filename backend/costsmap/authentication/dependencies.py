from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .schemas import UserOut
from .models import users
from .services import Authentication
from ..project.databases import database


auth_dependency = HTTPBearer()


async def get_token_user(credentials: HTTPAuthorizationCredentials = Depends(auth_dependency)):
    authentication = Authentication()
    user = await authentication.get_user_by_token(credentials.credentials)
    return user
