from .categories import GetCategoriesService, get_category_costs
from costs.services.costs import GetCostsTotalSumService


class GetCategoryCostsCommand:
    """Command to return category costs"""

    def __init__(self, category_pk, user):
        self._category_pk = category_pk
        self._user = user

    def execute(self) -> dict:
        """Return category costs, costs total sum and category itself
        in dict format
        """
        category = GetCategoriesService.get_concrete(
            self._category_pk, self._user
        )
        costs = get_category_costs(category)
        total_sum = GetCostsTotalSumService.execute(costs)
        return {'costs': costs, 'category': category, 'total_sum': total_sum}
