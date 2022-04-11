from pydantic import BaseModel, Field, validator, EmailStr


class Token(BaseModel):
    token: str = Field(..., description="JWT token")


class RegistrationAuthData(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

    @validator('password')
    def password_must_contain_different_cases(cls, v: str):
        if v.upper() == v or v.lower() == v:
            raise ValueError('password must contain different cases')

        return v

    @validator('password')
    def password_must_contain_numeric(cls, v: str):
        has_digit = any([str(num) in v for num in range(10)])
        if not has_digit:
            raise ValueError('password must contain at least one digit')

        return v

    @validator('password')
    def password_cant_contain_spaces(cls, v: str):
        has_spaces = any([space in v for space in (' ', '\t', '\r', '\n')])
        if has_spaces:
            raise ValueError('password can\'t contain spaces')

        return v


class LoginAuthData(BaseModel):
    email: EmailStr
    password: str
