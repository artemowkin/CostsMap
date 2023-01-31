from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select, delete, update

from .models import Category
from .schemas import CategoryIn
from ..authentication.models import User
from ..costs.models import Cost
from ..project.db import async_session


def _handle_unique_violation(func):
    """Decorator that handles unique violation error for categories"""

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT, "Category with this title already exists")

    return wrapper


def _handle_not_found_error(func):

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NoResultFound:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Category with this id for current user doesn't exist",
            )

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
        async with async_session() as session:
            stmt = select(Category).where(Category.owner_id == self._owner.uuid).order_by(Category.title)
            result = await session.execute(stmt)
            return result.scalars().all()

    @_handle_unique_violation
    async def create(self, category_data: CategoryIn) -> Category:
        """Creates new category for user
        
        :param category_data: Creating category data
        :raises: HTTPException(409) if category with this title already exists
        """
        async with async_session() as session:
            category = Category(**category_data.dict(), owner_id=self._owner.uuid)
            session.add(category)
            await session.commit()
            return category

    @_handle_not_found_error
    async def get_concrete(self, category_uuid: str) -> Category:
        """Returns concrete user category by id
        
        :param category_id: category uuid
        :raises: HTTPException(404) if category with this id for user doesn't exist
        :returns: Getted user category with this id
        """
        async with async_session() as session:
            stmt = select(Category).where(Category.owner_id == self._owner.uuid, Category.uuid == category_uuid)
            result = await session.execute(stmt)
            return result.scalar_one()

    async def delete_concrete(self, category: Category) -> None:
        """Deletes concrete user category
        
        :param category: Deleting category instance
        """
        async with async_session() as session:
            stmt = delete(Category).where(Category.uuid == category.uuid)
            await session.execute(stmt)
            await session.commit()

    @_handle_unique_violation
    async def update(self, category: Category, category_data: CategoryIn) -> Category:
        """Updates concrete user category
        
        :param category: Updating user category instance
        :param category_data: new category data
        :raises: HTTPException(409) if category with new title already exists
        :returns: Updated category instance
        """
        async with async_session() as session:
            stmt = update(Category).values(**category_data.dict()).where(Category.uuid == category.uuid)
            await session.execute(stmt)
            stmt = select(Category).where(Category.uuid == category.uuid)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()
