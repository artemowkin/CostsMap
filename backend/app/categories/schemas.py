from .models import Category


CategoryIn = Category.get_pydantic(exclude={'owner', 'uuid'})
