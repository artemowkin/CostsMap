from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from databases import Database

from project.db import get_database
from .schemas import (
    UserRegistration, UserLogIn, UserOut, ChangeUserPassword, UserIn
)
from .services import (
    create_user_in_db, create_token_for_user, check_user_password,
    decode_token, get_user_by_email, update_user_data, verify_password,
    update_user_password
)


oauth = OAuth2PasswordBearer(tokenUrl="token")


async def registrate_user(user: UserRegistration, db: Database = Depends(get_database)):
    """
    Create user in db if doesn't exist, generate and return
    the JWT token
    """
    await create_user_in_db(user, db)
    token = create_token_for_user(user.email)
    return token


async def login_user(user: UserLogIn, db: Database = Depends(get_database)):
    """Get user from db, check password and generate new jwt token"""
    await check_user_password(user, db)
    token = create_token_for_user(user.email)
    return token


async def get_current_user(token: str = Depends(oauth), db: Database = Depends(get_database)) -> UserOut:
    """Return current user using user email from token"""
    decoded_token = decode_token(token)
    db_user = await get_user_by_email(decoded_token['sub'], db)
    user = UserOut.from_orm(db_user)
    return user


async def change_user(
    changing_data: UserIn, token: str = Depends(oauth),
    db: Database = Depends(get_database)
) -> UserOut:
    """Change the current user using data from request"""
    decoded_token = decode_token(token)
    await update_user_data(decoded_token['sub'], changing_data, db)
    user_out = UserOut(**changing_data.dict())
    return user_out


async def change_user_password(
    changing_password: ChangeUserPassword, token: str = Depends(oauth),
    db: Database = Depends(get_database)
):
    """Change password for current user"""
    decoded_token = decode_token(token)
    db_user = await get_user_by_email(decoded_token['sub'], db)
    if not verify_password(changing_password.old_password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    await update_user_password(decoded_token['sub'], changing_password.new_password, db)