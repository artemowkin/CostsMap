from generics.views import (
    GetCreateGenericView, GetUpdateDeleteGenericView, GetForTheDateGenericView
)
from .services.base import (
    CreateIncomeService, GetIncomesService, DeleteIncomeService,
    ChangeIncomeService
)
from .services.commands import (
    GetAllIncomesCommand, GetIncomesForTheMonthCommand,
    GetIncomesForTheDateCommand
)
from .serializers import IncomeSerializer


class GetCreateIncomesView(GetCreateGenericView):
    """View to get all incomes and create a new income"""

    get_command = GetAllIncomesCommand
    create_service = CreateIncomeService
    serializer_class = IncomeSerializer
    model_name = 'income'


class GetUpdateDeleteIncome(GetUpdateDeleteGenericView):
    """View to get a concrete income and change/delete an existing income"""

    get_service_class = GetIncomesService
    delete_service_class = DeleteIncomeService
    update_service_class = ChangeIncomeService
    serializer_class = IncomeSerializer
    model_name = 'income'


class GetIncomesForTheMonthView(GetForTheDateGenericView):
    """View to get incomes for the month"""

    command = GetIncomesForTheMonthCommand


class GetIncomesForTheDateView(GetForTheDateGenericView):
    """View to get incomes for the date"""

    command = GetIncomesForTheDateCommand
