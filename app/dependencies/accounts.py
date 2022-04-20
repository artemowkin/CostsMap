from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from ..schemas.accounts import UserRegistration, UserLogIn, UserOut
from ..services.accounts import (
    create_user_in_db, create_token_for_user, check_user_password,
    decode_token, get_user_by_email, update_user_data
)


oauth = OAuth2PasswordBearer(tokenUrl="token")


async def registrate_user(user: UserRegistration):
    """
    Create user in DB if doesn't exist, generate and return
    the JWT token
    """
    await create_user_in_db(user)
    token = create_token_for_user(user.email)
    return token


async def login_user(user: UserLogIn):
    """Get user from DB, check password and generate new JWT token"""
    await check_user_password(user)
    token = create_token_for_user(user.email)
    return token


async def get_current_user(token: str = Depends(oauth)):
    """Return current user using user email from token"""
    decoded_token = decode_token(token)
    db_user = await get_user_by_email(decoded_token['sub'])
    user = UserOut.from_orm(db_user)
    return user


async def change_user(
    changing_data: UserOut, user: UserOut = Depends(get_current_user)
):
    """Change the current user using data from request"""
    await update_user_data(user.email, changing_data)
    return changing_data
