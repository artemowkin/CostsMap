from pydantic import BaseModel, Field


class Category(BaseModel):
    title: str = Field(..., max_length=50, min_length=1)

    class Config:
        orm_mode = True


class Category404(BaseModel):
    detail: str = 'Category with this title doesn\'t exist for current user'


class CategoryDeleted(BaseModel):
    deleted: bool


class Category400(BaseModel):
    detail: str
