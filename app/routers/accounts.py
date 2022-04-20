from fastapi import APIRouter, Depends

from ..schemas.accounts import Token
from ..dependencies.accounts import registrate_user


router = APIRouter()


@router.post("/registration/", response_model=Token)
async def registration(token: Token = Depends(registrate_user)):
    """Registrate user and generate JWT token"""
    return token
