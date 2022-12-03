from uuid import UUID

from pydantic import BaseModel, Field


class BaseCategory(BaseModel):
    title: str
    limit: float
    color: str = Field(..., regex=r"#[0-9a-f]{6}")


class CategoryOut(BaseCategory):
    uuid: UUID

    class Config:
        orm_mode = True


class CategoryIn(BaseCategory):
    ...
