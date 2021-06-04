from django.contrib.auth import get_user_model

from .base import GetCategoriesService, get_category_costs
from ..serializers import CategorySerializer
from costs.services.base import GetCostsTotalSumService


User = get_user_model()


class GetAllCategoriesCommand:
    """Command to get all categories"""

    get_service = GetCategoriesService
    serializer_class = CategorySerializer

    def __init__(self, user: User):
        self._user = user

    def execute(self) -> dict:
        service = self.get_service(self._user)
        categories = service.get_all()
        serialized_categories = self.serializer_class(
            categories, many=True
        ).data
        return {'categories': serialized_categories}


class GetCategoryCostsCommand:
    """Command to return category costs"""

    def __init__(self, category_pk, user):
        self._category_pk = category_pk
        self._user = user
        self._get_service = GetCategoriesService(user)
        self._total_sum_service = GetCostsTotalSumService()

    def execute(self) -> dict:
        """Return category costs, costs total sum and category itself
        in dict format
        """
        category = self._get_service.get_concrete(self._category_pk)
        costs = get_category_costs(category)
        total_sum = self._total_sum_service.execute(costs)
        return {'costs': costs, 'category': category, 'total_sum': total_sum}
