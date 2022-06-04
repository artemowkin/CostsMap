from pydantic import BaseModel, Field


class BaseCategory(BaseModel):
    """Base model for category"""
    title: str = Field(..., max_length=50)
    costs_limit: int | None = Field(None, gt=0, lt=1000000)
    color: str = Field(..., max_length=10)


class CategoryOut(BaseCategory):
    """Model for category in response"""
    id: int | None = None

    class Config:
        orm_mode = True
