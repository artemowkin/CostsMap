from fastapi import APIRouter, Depends

from ..schemas.accounts import Token
from ..dependencies.accounts import registrate_user, login_user


router = APIRouter()


@router.post("/registration/", response_model=Token)
async def registration(token: Token = Depends(registrate_user)):
    """Registrate user and generate JWT token"""
    return token


@router.post("/login/", response_model=Token)
async def login(token: Token = Depends(login_user)):
    """Log in user and generate new JWT token"""
    return token
