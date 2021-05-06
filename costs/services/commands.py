from django.contrib.auth import get_user_model

from .costs import GetCostsService, GetCostsTotalSumService
from ..serializers import CostSerializer


User = get_user_model()


class GetAllCostsCommand:
    """Command to get all user costs"""

    get_service = GetCostsService
    total_sum_service = GetCostsTotalSumService()
    serializer_class = CostSerializer

    def __init__(self, user: User):
        self._user = user
        self._service = self.get_service(user)

    def execute(self) -> dict:
        all_costs = self._service.get_all()
        total_costs_sum = self.total_sum_service.execute(all_costs)
        serialized_costs = self.serializer_class(all_costs, many=True).data
        return {
            'total_sum': total_costs_sum, 'costs': serialized_costs
        }
