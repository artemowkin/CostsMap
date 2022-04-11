from fastapi import APIRouter, Depends

from app.schemas.accounts import Token
from app.dependencies.accounts import authenticate_user, registrate_user


router = APIRouter()


@router.post("/login", response_model=Token)
async def login_user(token: Token = Depends(authenticate_user)):
    """
    Login user using `username` and `password` fields in JSON
    request
    """
    return {'token': token}


@router.post("/registration", response_model=Token)
async def reg_user(token: Token = Depends(registrate_user)):
    """
    Registrate user using `username`, `password1`, and `password2`
    fields in JSON request
    """
    return {'token': token}
