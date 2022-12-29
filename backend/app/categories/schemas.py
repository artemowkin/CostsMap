from .models import Category


CategoryIn = Category.get_pydantic(exclude={'owner', 'uuid'})

BaseCategoryOut = Category.get_pydantic(exclude={'owner'})

class CategoryOut(BaseCategoryOut):
    costs_sum: int
