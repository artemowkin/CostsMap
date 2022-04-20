from ..schemas.accounts import UserRegistration
from ..services.accounts import create_user_in_db, create_token_for_user


async def registrate_user(user: UserRegistration):
    """
    Create user in DB if doesn't exist, generate and return
    the JWT token
    """
    await create_user_in_db(user)
    token = create_token_for_user(user.email)
    return token
