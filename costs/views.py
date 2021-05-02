import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from .services.costs import (
    CreateCostService, GetCostsService, DeleteCostService
)
from .serializers import CostSerializer
from categories.models import Category


class GetCreateCostsView(APIView):
    """View to get all costs and create a new cost"""

    get_service = GetCostsService
    create_service = CreateCostService
    serializer_class = CostSerializer

    def get(self, request):
        service = self.get_service(request.user)
        all_costs = service.get_all()
        serializer = self.serializer_class(all_costs, many=True)
        return Response(serializer.data)

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
    serializer_class = CostSerializer

    def get(self, request, pk):
        service = self.get_service(request.user)
        cost = service.get_concrete(pk)
        serializer = self.serializer_class(cost)
        return Response(serializer.data)

    def delete(self, request, pk):
        get_concrete_service = self.get_service(request.user)
        cost = get_concrete_service.get_concrete(pk)
        self.delete_service.execute({'cost': cost})
        return Response(status=204)


class GetForTheDateView(APIView):
    """View to get costs for the date"""

    pass


class CostsDateStatisticView(APIView):
    """View to get costs statistic for the date"""

    pass


class AverageCostsView(APIView):
    """View to get an average costs"""

    pass
