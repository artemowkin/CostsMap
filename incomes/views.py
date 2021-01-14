from rest_framework.response import Response

from .serializers import PostIncomeSerializer
from .services.commands import (
    GetIncomesStatisticCommand, GetIncomesForTheDateCommand,
    GetIncomesHistoryCommand
)
from incomes.services import (
    GetIncomesService, DeleteIncomeService, CreateIncomeService,
    ChangeIncomeService
)
from utils.views import (
    StatisticPageGenericView, DateGenericView, HistoryGenericView,
    DeleteGenericView, DefaultView
)


class IncomesForTheDateView(DateGenericView):
    """View to return user incomes for the date"""

    command = GetIncomesForTheDateCommand


class CreateIncomeView(DefaultView):
    """View to create a new income"""

    serializer = PostIncomeSerializer

    def post(self, request):
        request_data = request.data.copy()
        request_data.update({'owner': request.user.pk})
        serializer = self.serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        income = CreateIncomeService.execute(request_data)
        return Response(serializer.data, status=201)


class ChangeIncomeView(DefaultView):
    """View to change a concrete income"""

    serializer = PostIncomeSerializer

    def post(self, request, pk):
        request_data = request.data.copy()
        request_data.update({'owner': request.user.pk})
        income = GetIncomesService.get_concrete(pk, request.user)
        serializer = self.serializer(income, data=request_data)
        serializer.is_valid(raise_exception=True)
        request_data.update({'income': income})
        income = ChangeIncomeService.execute(request_data)
        return Response(serializer.data, status=200)


class DeleteIncomeView(DeleteGenericView):
    """View to delete a concrete income"""

    object_name = 'income'
    get_service = GetIncomesService
    delete_service = DeleteIncomeService


class IncomesHistoryView(HistoryGenericView):
    """View to return all user incomes"""

    command = GetIncomesHistoryCommand


class IncomesStatisticPageView(StatisticPageGenericView):
    """View to return statistic with user incomes for the month"""

    command = GetIncomesStatisticCommand
