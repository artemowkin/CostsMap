from .categories import GetCategoriesService, get_category_costs
from costs.services.costs import GetCostsTotalSumService


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
