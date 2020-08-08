"""Module with costs views"""

from django.shortcuts import render
from django.http import JsonResponse

from utils.views import (
    APIAuthorizedView,
    DateView,
    HistoryView,
    CreateView,
    ChangeView,
    DeleteView,
    StatisticPageView
)

from .services import CostService


class CostsForTheDateView(DateView):

    """View to return costs for the date

    Attributes
    ----------
    service : Service
        Cost service

    template_name : str
        Template to display costs for the date

    context_object_name : str
        Name of costs in template

    """

    service = CostService()
    template_name = 'costs/costs.html'
    context_object_name = 'costs'


class CostsHistoryView(HistoryView):

    """View to return all costs for all time.

    Attributes
    ----------
    service : Service
        Cost service

    template_name : str
        Template to display history of costs

    context_object_name : str
        Name of costs in template

    """

    service = CostService()
    template_name = 'costs/history_costs.html'
    context_object_name = 'costs'


class CreateCostView(CreateView):

    """View to create a new cost

    Attributes
    ----------
    service : Service
        Cost's service

    template_name : str
        Template with form to create a cost

    """

    service = CostService()
    template_name = 'costs/add_cost.html'

    def get(self, request):
        """Return create cost form"""
        form = self.service.get_create_form(owner=request.user)
        return render(request, self.template_name, {'form': form})


class ChangeCostView(ChangeView):

    """View to change a cost

    Attributes
    ----------
    service : Service
        Cost's service

    template_name : str
        Template with form to change a cost

    context_object_name : str
        Name of cost object in template

    """

    service = CostService()
    template_name = 'costs/change_cost.html'
    context_object_name = 'cost'


class DeleteCostView(DeleteView):

    """View to delete a cost

    Attributes
    ----------
    service : Service
        Cost's service

    template_name : str
        Template with confirmation form to delete an instance

    context_object_name : str
        Name of cost object in template

    """

    service = CostService()
    template_name = 'costs/delete_cost.html'
    context_object_name = 'cost'


class StatisticView(APIAuthorizedView):

    """View to return json with costs statistic

    Attributes
    ----------
    service : Service
        Cost's service

    """

    service = CostService()

    def get(self, request, date):
        """Return json with cost's statistic for the month"""
        data = self.service.get_statistic_for_the_month(
            owner=request.user, date=date
        )
        return JsonResponse(data, safe=False)


class CostsStatisticPageView(StatisticPageView):

    """View to return statistic with costs for the month

    Attributes
    ----------
    service : Service
        Cost's service

    template_name : str
        Template to display statistic with costs

    context_object_name : str
        Name of costs in template

    """

    service = CostService()
    cost_service = CostService()
    template_name = 'costs/costs_statistic.html'
    context_object_name = 'costs'

