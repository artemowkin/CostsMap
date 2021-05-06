import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from .services.costs import (
    CreateCostService, GetCostsService, DeleteCostService, ChangeCostService,
    GetCostsForTheDateService, GetStatisticForTheMonthService,
    GetStatisticForTheYearService, GetCostsTotalSumService,
    GetAverageCostsForTheDayService
)
from .services.commands import (
    GetAllCostsCommand, GetCostsForTheMonthCommand, GetCostsForTheDateCommand,
)
from .serializers import CostSerializer
from categories.models import Category


class GetCreateCostsView(APIView):
    """View to get all costs and create a new cost"""

    get_command = GetAllCostsCommand
    get_service = GetCostsService
    create_service = CreateCostService
    total_sum_service = GetCostsTotalSumService()
    serializer_class = CostSerializer

    def get(self, request):
        command = self.get_command(request.user)
        data = command.execute()
        return Response(data)

    def post(self, request):
        cost_data = request.data | {'owner': request.user}
        serializer = self.serializer_class(data=cost_data)
        if serializer.is_valid():
            cost = self.create_service.execute(cost_data)
            return Response({'cost': cost.pk}, status=201)

        return Response(serializer.errors, status=400)


class GetUpdateDeleteCost(APIView):
    """View to get a concrete cost and change/delete an existing cost"""

    get_service = GetCostsService
    delete_service = DeleteCostService
    update_service = ChangeCostService
    serializer_class = CostSerializer

    def get(self, request, pk):
        service = self.get_service(request.user)
        cost = service.get_concrete(pk)
        serializer = self.serializer_class(cost)
        return Response(serializer.data)

    def delete(self, request, pk):
        get_concrete_service = self.get_service(request.user)
        cost = get_concrete_service.get_concrete(pk)
        self.delete_service.execute({'cost': cost, 'owner': request.user})
        return Response(status=204)

    def put(self, request, pk):
        get_concrete_service = self.get_service(request.user)
        cost = get_concrete_service.get_concrete(pk)
        serializer = self.serializer_class(cost, data=request.data)
        if serializer.is_valid():
            service_data = serializer.validated_data | {
                'cost': cost, 'owner': request.user
            }
            self.update_service.execute(service_data)
            return Response(status=204)

        return Response(serializer.errors, status=400)


class GetForTheMonthView(APIView):
    """View to get costs for the month"""

    command = GetCostsForTheMonthCommand

    def get(self, request, year, month):
        date = datetime.date(year, month, 1)
        command = self.command(request.user, date)
        costs = command.execute()
        return Response(costs)


class GetForTheDateView(APIView):
    """View to get costs for the date"""

    command = GetCostsForTheDateCommand

    def get(self, request, year, month, day):
        date = datetime.date(year, month, day)
        command = self.command(request.user, date)
        costs = command.execute()
        return Response(costs)


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
