from fastapi import APIRouter, Depends

from .schemas import TokenPair, LoginData, RegistrationData
from .dependencies import use_auth_store, use_token
from .services import AuthStore
from .models import User


router = APIRouter()


@router.post('/login/', response_model=TokenPair)
async def login(login_data: LoginData, auth_store: AuthStore = Depends(use_auth_store)):
    token_pair = await auth_store.login(login_data)
    return token_pair


@router.post('/registration/', response_model=TokenPair)
async def registration(registration_data: RegistrationData, auth_store: AuthStore = Depends(use_auth_store)):
    token_pair = await auth_store.registrate(registration_data)
    return token_pair


@router.post('/refresh/', response_model=TokenPair)
async def refresh(token: str = Depends(use_token), auth_store: AuthStore = Depends(use_auth_store)):
    token_pair = await auth_store.refresh(token)
    return token_pair


@router.get('/me/', response_model=User.get_pydantic(exclude={'password'}))
async def me(token: str = Depends(use_token), auth_store: AuthStore = Depends(use_auth_store)):
    user = await auth_store.get_user_from_token(token)
    return user


@router.post('/logout/', status_code=204)
async def logout(token: str = Depends(use_token), auth_store: AuthStore = Depends(use_auth_store)):
    await auth_store.logout(token)