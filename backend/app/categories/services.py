from fastapi import HTTPException, status
from ormar import NoMatch
from asyncpg.exceptions import UniqueViolationError

from .models import Category
from .schemas import CategoryIn
from ..authentication.models import User
from ..costs.models import Cost


def _handle_unique_violation(func):
    """Decorator that handles unique violation error for categories"""

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except UniqueViolationError:
            raise HTTPException(status.HTTP_409_CONFLICT, "Category with this title already exists")

    return wrapper


class CategoriesSet:
    """Service with logic for categories
    
    :param owner: Current user
    """

    def __init__(self, owner: User):
        self._model = Category
        self._costs_model = Cost
        self._owner = owner

    async def all(self) -> list[Category]:
        """Returns all user categories
        
        :returns: All categories filtered by user
        """
        all_categories = await self._model.objects.filter(owner__uuid=self._owner.uuid).order_by('title').all()
        return all_categories

    @_handle_unique_violation
    async def create(self, category_data: CategoryIn) -> Category:
        """Creates new category for user
        
        :param category_data: Creating category data
        :raises: HTTPException(409) if category with this title already exists
        """
        category = await self._model.objects.create(**category_data.dict(), owner=self._owner)
        return category

    async def get_concrete(self, category_id: str) -> Category:
        """Returns concrete user category by id
        
        :param category_id: category id
        :raises: HTTPException(404) if category with this id for user doesn't exist
        :returns: Getted user category with this id
        """
        try:
            return await self._model.objects.get(owner__uuid=self._owner.uuid, uuid=category_id)
        except NoMatch:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Category with this id for current user doesn't exist"
            )

    async def delete_concrete(self, category: Category) -> None:
        """Deletes concrete user category
        
        :param category: Deleting category instance
        """
        await category.delete()

    @_handle_unique_violation
    async def update(self, category: Category, category_data: CategoryIn) -> Category:
        """Updates concrete user category
        
        :param category: Updating user category instance
        :param category_data: new category data
        :raises: HTTPException(409) if category with new title already exists
        :returns: Updated category instance
        """
        await category.update(**category_data.dict())
        await category.load()
        return category
