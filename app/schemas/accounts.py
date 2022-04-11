from pydantic import BaseModel, Field, validator, EmailStr


class Token(BaseModel):
    token: str = Field(..., description="JWT token")


class LoginAuthData(BaseModel):
    email: EmailStr
    password: str


class RegistrationAuthData(BaseModel):
    email: EmailStr
    password1: str = Field(..., min_length=8, max_length=128)
    password2: str = Field(..., min_length=8, max_length=128)

    @validator('password1')
    def password_must_contain_different_cases(cls, v: str):
        if v.upper() == v or v.lower() == v:
            raise ValueError('password must contain different cases')

        return v

    @validator('password1')
    def password_must_contain_numeric(cls, v: str):
        has_digit = any([str(num) in v for num in range(10)])
        if not has_digit:
            raise ValueError('password must contain at least one digit')

        return v

    @validator('password1')
    def password_cant_contain_spaces(cls, v: str):
        has_spaces = any([space in v for space in (' ', '\t', '\r', '\n')])
        if has_spaces:
            raise ValueError('password can\'t contain spaces')

        return v

    @validator('password2')
    def passwords_must_be_equal(cls, v: str, values: dict, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')

        return v


class User(BaseModel):
    id: int
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
