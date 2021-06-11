import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from generics.views import (
    GetCreateGenericView, GetUpdateDeleteGenericView, GetForTheDateGenericView
)
from .services.base import (
    CreateCostService, GetCostsService, DeleteCostService, ChangeCostService,
    GetStatisticForTheMonthService, GetStatisticForTheYearService,
    GetAverageCostsForTheDayService
)
from .services.commands import (
    GetAllCostsCommand, GetCostsForTheMonthCommand, GetCostsForTheDateCommand,
)
from .serializers import CostSerializer


class GetCreateCostsView(GetCreateGenericView):
    """View to get all costs and create a new cost"""

    get_command = GetAllCostsCommand
    create_service = CreateCostService
    serializer_class = CostSerializer
    model_name = 'cost'


class GetUpdateDeleteCost(GetUpdateDeleteGenericView):
    """View to get a concrete cost and change/delete an existing cost"""

    get_service_class = GetCostsService
    delete_service_class = DeleteCostService
    update_service_class = ChangeCostService
    serializer_class = CostSerializer
    model_name = 'cost'


class GetCostsForTheMonthView(GetForTheDateGenericView):
    """View to get costs for the month"""

    command = GetCostsForTheMonthCommand


class GetCostsForTheDateView(GetForTheDateGenericView):
    """View to get costs for the date"""

    command = GetCostsForTheDateCommand


class CostsMonthStatisticView(APIView):
    """View to get costs statistic for the month"""

    service_class = GetStatisticForTheMonthService

    def get(self, request, year, month):
        date = datetime.date(year, month, 1)
        service_data = {'user': request.user, 'date': date}
        statistic = self.service_class.execute(service_data)
        return Response(statistic)


class CostsYearStatisticView(APIView):
    """View to get costs statistic for the year"""

    service_class = GetStatisticForTheYearService

    def get(self, request, year):
        date = datetime.date(year, 1, 1)
        service_data = {'user': request.user, 'date': date}
        statistic = self.service_class.execute(service_data)
        return Response(statistic)


class AverageCostsView(APIView):
    """View to get an average costs"""

    average_service = GetAverageCostsForTheDayService

    def get(self, request):
        average_costs = self.average_service.execute({'user': request.user})
        return Response({'average_costs': average_costs})
