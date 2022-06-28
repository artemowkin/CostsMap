from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from .schemas import (
    UserRegistration, UserLogIn, UserOut, ChangeUserPassword, UserIn
)
from .models import Users
from .services import (
    create_user_in_db, create_token_for_user, check_user_password,
    decode_token, get_user_by_email, update_user_data, verify_password,
    update_user_password
)


oauth = OAuth2PasswordBearer(tokenUrl="token")


async def registrate_user(user: UserRegistration):
    """
    Create user in db if doesn't exist, generate and return
    the JWT token
    """
    await create_user_in_db(user)
    token = create_token_for_user(user.email)
    return token


async def login_user(user: UserLogIn):
    """Get user from db, check password and generate new jwt token"""
    await check_user_password(user)
    token = create_token_for_user(user.email)
    return token


async def get_current_user(token: str = Depends(oauth)) -> Users:
    """Return current user using user email from token"""
    decoded_token = decode_token(token)
    db_user = await get_user_by_email(decoded_token['sub'])
    return db_user


async def change_user(
    changing_data: UserIn, current_user: Users = Depends(get_current_user)
) -> UserOut:
    """Change the current user using data from request"""
    await update_user_data(current_user.id, changing_data)
    user_out = UserOut(id=current_user.id, **changing_data.dict())
    return user_out


async def change_user_password(
    changing_password: ChangeUserPassword, token: str = Depends(oauth)
):
    """Change password for current user"""
    decoded_token = decode_token(token)
    db_user = await get_user_by_email(decoded_token['sub'])
    if not verify_password(changing_password.old_password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    await update_user_password(decoded_token['sub'], changing_password.new_password)
