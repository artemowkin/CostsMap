from fastapi import APIRouter, Depends

from .schemas import (
    Token, UserOut, SupportedCurrencies, SupportedLanguages
)
from .dependencies import (
    registrate_user, login_user, get_current_user, change_user,
    change_user_password
)


router = APIRouter()


@router.post("/registration/", response_model=Token)
def registration(token: Token = Depends(registrate_user)):
    """Registrate user and generate JWT token"""
    return token


@router.post("/login/", response_model=Token)
def login(token: Token = Depends(login_user)):
    """Log in user and generate new JWT token"""
    return token


@router.get("/me/", response_model=UserOut)
def me(user: UserOut = Depends(get_current_user)):
    """Change current user data"""
    return user


@router.put("/me/", response_model=UserOut)
def me(user: UserOut = Depends(change_user)):
    """Change current user data"""
    return user


@router.post(
    "/change_password/",
    dependencies=[Depends(change_user_password)],
    status_code=204
)
def change_password():
    """Change password for user"""
    pass


@router.get("/languages/", response_model=SupportedLanguages)
def languages():
    """List of all supported languages"""
    return SupportedLanguages()


@router.get("/currencies/", response_model=SupportedCurrencies)
def currencies():
    """List of all supported currencies"""
    return SupportedCurrencies()
