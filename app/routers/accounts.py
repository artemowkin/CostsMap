from fastapi import APIRouter, Depends

from app.schemas.accounts import Token
from app.dependencies.accounts import authenticate_user


router = APIRouter()


@router.post("/login", response_model=Token)
async def login_user(token: Token = Depends(authenticate_user)):
    """
    Login user using `username` and `password` fields in JSON
    request
    """
    return {'token': token}
