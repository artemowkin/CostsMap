from pydantic import BaseModel, Field


class Category(BaseModel):
    title: str = Field(..., max_length=50, min_length=1)
