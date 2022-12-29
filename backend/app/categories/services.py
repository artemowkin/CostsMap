from fastapi import HTTPException, status
from ormar import NoMatch
from asyncpg.exceptions import UniqueViolationError

from .models import Category
from .schemas import CategoryIn
from ..authentication.models import User


def _handle_unique_violation(func):

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except UniqueViolationError:
            raise HTTPException(status.HTTP_409_CONFLICT, "Category with this title already exists")

    return wrapper


class CategoriesSet:

    def __init__(self, owner: User):
        self._model = Category
        self._owner = owner

    async def all(self) -> list[Category]:
        all_categories = await self._model.objects.filter(owner__uuid=self._owner.uuid).order_by('title').all()
        return all_categories

    async def get_costs_sum(self, category: Category) -> int:
        return 0

    @_handle_unique_violation
    async def create(self, category_data: CategoryIn) -> Category:
        category = await self._model.objects.create(**category_data.dict(), owner=self._owner)
        return category

    async def get_concrete(self, category_id: str) -> Category:
        try:
            return await self._model.objects.get(owner__uuid=self._owner.uuid, uuid=category_id)
        except NoMatch:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Category with this id for current user doesn't exist"
            )

    async def delete_concrete(self, category: Category) -> None:
        await category.delete()

    @_handle_unique_violation
    async def update(self, category: Category, category_data: CategoryIn) -> Category:
        await category.update(**category_data.dict())
        await category.load()
        return category
