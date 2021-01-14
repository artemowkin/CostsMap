from rest_framework.response import Response

from ..serializers import PostCostSerializer
from ..services.commands import GetCostsStatisticCommand
from costs.services import (
    GetCostsService, CreateCostService, ChangeCostService, DeleteCostService,
    GetStatisticForTheMonthService, GetStatisticForTheYearService
)
from costs.services.commands import (
    GetCostsForTheDateCommand, GetCostsHistoryCommand
)
from utils.views import (
    DefaultView, DeleteGenericView, StatisticPageGenericView,
    DateGenericView, HistoryGenericView
)


class CostsForTheDateView(DateGenericView):
    """View to return costs for the date"""

    command = GetCostsForTheDateCommand


class CostsHistoryView(HistoryGenericView):
    """View to return all costs for all time"""

    command = GetCostsHistoryCommand


class CreateCostView(DefaultView):
    """View to create a new cost"""

    serializer = PostCostSerializer

    def post(self, request):
        request_data = request.data.copy()
        request_data.update({'owner': request.user.pk})
        serializer = self.serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        cost = CreateCostService.execute(request_data)
        return Response(serializer.data, status=201)


class ChangeCostView(DefaultView):
    """View to change a concrete cost"""

    serializer = PostCostSerializer

    def post(self, request, pk):
        request_data = request.data.copy()
        request_data.update({'owner': request.user.pk})
        cost = GetCostsService.get_concrete(pk, request.user)
        serializer = self.serializer(cost, data=request_data)
        serializer.is_valid(raise_exception=True)
        request_data.update({'cost': cost})
        cost = ChangeCostService.execute(request_data)
        return Response(serializer.data)


class DeleteCostView(DeleteGenericView):
    """View to delete a concrete cost"""

    object_name = 'cost'
    get_service = GetCostsService
    delete_service = DeleteCostService


class CostsStatisticForTheMonthView(DefaultView):
    """View to return json with costs statistic for the month"""

    def get(self, request, date):
        data = GetStatisticForTheMonthService.execute({
            'user': request.user,
            'date': date
        })
        return Response(data)


class CostsStatisticPageView(StatisticPageGenericView):
    """View to return statistic with costs for the month by categories"""

    command = GetCostsStatisticCommand


class CostsStatisticForTheYear(DefaultView):
    """View to return statistic with costs by months for the year"""

    def get(self, request, date):
        data = GetStatisticForTheYearService.execute({
            'user': request.user,
            'date': date
        })
        return Response(data)
