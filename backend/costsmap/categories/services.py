from uuid import uuid4

from asyncpg.exceptions import UniqueViolationError
from fastapi import HTTPException, status

from .models import categories
from .schemas import CategoryIn, CategoryOut
from ..project.databases import database


class CategoriesSet:

    table = categories

    async def create(self, category_data: CategoryIn) -> CategoryOut:
        uuid = str(uuid4())
        query = self.table.insert().values(uuid=uuid, **category_data.dict())
        try:
            await database.execute(query)
            return CategoryOut(uuid=uuid, **category_data.dict())
        except UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Category with this title already exists"
            )

    async def get_all(self) -> list[CategoryOut]:
        query = self.table.select()
        result = await database.fetch_all(query)
        result_schemas = [CategoryOut.from_orm(category) for category in result]
        return result_schemas
