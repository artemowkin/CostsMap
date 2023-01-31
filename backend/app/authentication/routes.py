from fastapi import APIRouter, Depends, Cookie

from .schemas import TokenPair, LoginData, RegistrationData, UserOut
from .dependencies import use_auth_store, use_token, auth_required
from .services import AuthStore


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
async def refresh(refresh_token: str = Cookie(...), auth_store: AuthStore = Depends(use_auth_store)):
    token_pair = await auth_store.refresh(refresh_token)
    return token_pair


@router.get('/me/', response_model=UserOut)
async def me(user: UserOut = Depends(auth_required)):
    return UserOut.from_orm(user)


@router.post('/logout/', status_code=204)
async def logout(token: str = Depends(use_token), auth_store: AuthStore = Depends(use_auth_store)):
    await auth_store.logout(token)
