from rest_framework.views import APIView

from .services.commands import (
    GetAllIncomesCommand
)


class GetCreateIncomesView(APIView):
    """View to get all incomes or create a new income"""

    get_command = GetAllIncomesCommand
    create_service = CreateIncomeService
    serializer_class = IncomeSerializer

    def get(self, request):
        command = self.get_command(request.user)
        data = command.execute()
        return Response(data)


class GetUpdateDeleteIncome(APIView):
    """View to get/update/delete a concrete income"""

    pass


class GetIncomesForTheMonthView(APIView):
    """View to get incomes for the month"""

    pass


class GetIncomesForTheDateView(APIView):
    """View to get incomes for the concrete date"""

    pass
