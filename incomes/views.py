import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from .services.base import (
    CreateIncomeService, GetIncomesService, DeleteIncomeService,
    ChangeIncomeService
)
from .services.commands import (
    GetAllIncomesCommand, GetIncomesForTheMonthCommand,
    GetIncomesForTheDateCommand
)
from .serializers import IncomeSerializer


class GetCreateIncomesView(APIView):
    """View to get all incomes and create a new income"""

    get_command = GetAllIncomesCommand
    create_service = CreateIncomeService
    serializer_class = IncomeSerializer

    def get(self, request):
        command = self.get_command(request.user)
        data = command.execute()
        return Response(data)

    def post(self, request):
        income_data = request.data | {'owner': request.user}
        serializer = self.serializer_class(data=income_data)
        if serializer.is_valid():
            income = self.create_service.execute(income_data)
            return Response({'income': income.pk}, status=201)

        return Response(serializer.errors, status=400)


class GetUpdateDeleteIncome(APIView):
    """View to get a concrete income and change/delete an existing income"""

    get_service = GetIncomesService
    delete_service = DeleteIncomeService
    update_service = ChangeIncomeService
    serializer_class = IncomeSerializer

    def get(self, request, pk):
        service = self.get_service(request.user)
        income = service.get_concrete(pk)
        serializer = self.serializer_class(income)
        return Response(serializer.data)

    def delete(self, request, pk):
        get_concrete_service = self.get_service(request.user)
        income = get_concrete_service.get_concrete(pk)
        self.delete_service.execute({'income': income, 'owner': request.user})
        return Response(status=204)

    def put(self, request, pk):
        get_concrete_service = self.get_service(request.user)
        income = get_concrete_service.get_concrete(pk)
        serializer = self.serializer_class(income, data=request.data)
        if serializer.is_valid():
            service_data = serializer.validated_data | {
                'income': income, 'owner': request.user
            }
            self.update_service.execute(service_data)
            return Response(status=204)

        return Response(serializer.errors, status=400)


class GetIncomesForTheMonthView(APIView):
    """View to get incomes for the month"""

    command = GetIncomesForTheMonthCommand

    def get(self, request, year, month):
        date = datetime.date(year, month, 1)
        command = self.command(request.user, date)
        incomes = command.execute()
        return Response(incomes)


class GetIncomesForTheDateView(APIView):
    """View to get incomes for the date"""

    command = GetIncomesForTheDateCommand

    def get(self, request, year, month, day):
        date = datetime.date(year, month, day)
        command = self.command(request.user, date)
        incomes = command.execute()
        return Response(incomes)
