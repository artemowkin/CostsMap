from fastapi import APIRouter, Depends

from .schemas import TokenPair, LoginData
from .dependencies import use_auth_store
from .services import AuthStore


router = APIRouter()


@router.post('/login/', response_model=TokenPair)
async def login(login_data: LoginData, auth_store: AuthStore = Depends(use_auth_store)):
    token_pair = await auth_store.login(login_data)
    return token_pair
