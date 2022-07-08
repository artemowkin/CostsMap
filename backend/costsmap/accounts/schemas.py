from typing import Literal
from enum import Enum

from pydantic import EmailStr, Field, validator

from ..project.schemas import CamelModel


def _validate_password_constratints(password: str):
    """Validate constratints for password"""
    if password.lower() == password:
        raise ValueError('Password must contain different cases')

    if not [char for char in password if char.isdigit()]:
        raise ValueError('Password must contain numbers')


class Currencies(str, Enum):
    """Enumeration of available currencies"""

    ruble = '₽'
    dollar = '$'
    euro = '€'
    yuan = '¥'


class SupportedCurrencies(CamelModel):
    """Model that has list of supported currencies"""

    currencies: list[str] = ['₽', '$', '€', '¥']


class BaseUser(CamelModel):
    """Base user pydantic model with base fields"""

    email: EmailStr = Field(..., description='user email')


class UserIn(BaseUser):
    """User pydantic model for input request data"""

    currency: Currencies = Field(..., description='main user currency')


class UserOut(UserIn):
    """User pydantic model for sending user info as response"""

    id: int

    class Config(UserIn.Config):
        orm_mode = True


class UserLogIn(BaseUser):
    """User pydantic model with data to log in"""

    password: str = Field(
        ..., min_length=6, max_length=256,
        description='logging in user password'
    )


class UserRegistration(BaseUser):
    """User pydantic model with data for registration"""

    currency: Currencies = Field(..., description='main user currency')
    password1: str = Field(
        ..., min_length=6, max_length=256, description='user password'
    )
    password2: str = Field(
        ..., min_length=6, max_length=256, description='user password repeat'
    )

    @validator('password1')
    def password_constraints(cls, v):
        _validate_password_constratints(v)
        return v

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        # Skip liter warning
        (kwargs)
        if 'password1' in values and v != values['password1']:
            raise ValueError('Passwords do not match')

        return v


class ChangeUserPassword(CamelModel):
    """Pydantic model with data for changing user password"""

    old_password: str = Field(..., description="old user password")
    new_password: str = Field(..., min_length=6, max_length=256, description="new user password")

    @validator('new_password')
    def password_constraints(cls, v):
        _validate_password_constratints(v)
        return v

    @validator('new_password')
    def passwords_do_not_match(cls, v, values):
        if 'old_password' in values and v == values['old_password']:
            raise ValueError('Passwords are the same')

        return v


class Token(CamelModel):
    """Model with token information"""

    token: str = Field(..., description="string with token")
    exptime: int = Field(..., description="expires date for token")


class UniqueUserEmailError(CamelModel):
    detail: Literal["User with this email already exists"]


class Login400Response(CamelModel):
    detail: Literal["Incorrect password"]


class ChangePassword400Response(CamelModel):
    detail: Literal["Incorrect old password"]


class LoginRequiredResponse(CamelModel):
    detail: Literal["Not authenticated"]
