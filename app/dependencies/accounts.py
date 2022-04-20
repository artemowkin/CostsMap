from ..schemas.accounts import UserRegistration, UserLogIn
from ..services.accounts import (
    create_user_in_db, create_token_for_user, check_user_password
)


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
