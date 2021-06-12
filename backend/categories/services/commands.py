from django.contrib.auth import get_user_model

from .base import GetCategoriesService, get_category_costs
from ..serializers import CategorySerializer
from costs.services.base import GetCostsTotalSumService
from costs.serializers import ImmutableCostSerializer


User = get_user_model()


class GetAllCategoriesCommand:
    """Command to get all categories"""

    get_service = GetCategoriesService
    serializer_class = CategorySerializer

    def __init__(self, user: User):
        self._user = user

    def execute(self) -> list:
        service = self.get_service(self._user)
        categories = service.get_all()
        serialized_categories = self.serializer_class(
            categories, many=True
        ).data
        return serialized_categories


class GetCategoryCostsCommand:
    """Command to return category costs"""

    get_service_class = GetCategoriesService
    total_sum_service = GetCostsTotalSumService()
    cost_serializer = ImmutableCostSerializer
    category_serializer = CategorySerializer

    def __init__(self, category_pk, user):
        self._category_pk = category_pk
        self._user = user
        self.get_service = self.get_service_class(user)

    def execute(self) -> dict:
        """Return category costs, costs total sum and category itself
        in dict format
        """
        category = self.get_service.get_concrete(self._category_pk)
        costs = get_category_costs(category)
        serialized_costs = self.cost_serializer(costs, many=True).data
        total_sum = self.total_sum_service.execute(costs)
        return {
            'costs': serialized_costs, 'category': category.title,
            'total_sum': total_sum
        }
