from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials

from .schemas import UserRegistration, UserLogin, Token, UserOut
from .services import Authentication
from .dependencies import get_token_user, auth_dependency


router = APIRouter()


@router.post('/registration', response_model=Token)
async def registrate_user(user_data: UserRegistration):
    authentication = Authentication()
    token = await authentication.registrate(user_data)
    return token


@router.post('/login', response_model=Token)
async def login_user(user_data: UserLogin):
    authentication = Authentication()
    token = await authentication.login(user_data)
    return token


@router.get('/me', response_model=UserOut)
async def current_user(user: UserOut = Depends(get_token_user)):
    return user


@router.post('/refresh', response_model=Token)
async def refresh(credentials: HTTPAuthorizationCredentials = Depends(auth_dependency)):
    authentication = Authentication()
    token = await authentication.refresh_tokens(credentials.credentials)
    return token
