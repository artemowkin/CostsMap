from uuid import UUID

from .models import Income


BaseIncome = Income.get_pydantic(exclude={'uuid', 'owner', 'category', 'card', 'pub_datetime'})


class IncomeIn(BaseIncome):
    card: UUID