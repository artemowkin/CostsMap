from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy

from .forms import CostForm
from .services.commands import GetCostsStatisticCommand
from costs.services import (
    GetCostsService, CreateCostService, ChangeCostService, DeleteCostService,
    GetStatisticForTheMonthService, GetStatisticForTheYearService
)
from categories.services.categories import (
    GetCategoriesService, set_form_categories
)
from costs.services.commands import (
    GetCostsForTheDateCommand, GetCostsHistoryCommand
)
from utils.views import (
    DefaultView, DeleteGenericView, StatisticPageGenericView,
    DateGenericView, HistoryGenericView
)


class CostsForTheDateView(DateGenericView):
    """View to render costs for the date"""

    template_name = 'costs/costs.html'
    command = GetCostsForTheDateCommand


class CostsHistoryView(HistoryGenericView):
    """View to render all costs for all time."""

    template_name = 'costs/history_costs.html'
    command = GetCostsHistoryCommand


class CreateCostView(DefaultView):
    """View to create a new cost"""

    form_class = CostForm
    template_name = 'costs/add_cost.html'

    def get(self, request):
        form = self.form_class()
        get_categories_service = GetCategoriesService(request.user)
        user_categories = get_categories_service.get_all()
        set_form_categories(form, user_categories)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        get_categories_service = GetCategoriesService(request.user)
        user_categories = get_categories_service.get_all()
        set_form_categories(form, user_categories)
        if form.is_valid():
            return self.form_valid(request, form)

        return render(request, self.template_name, {'form': form})

    def form_valid(self, request, form):
        form.cleaned_data.update({'owner': request.user})
        cost = CreateCostService.execute(form.cleaned_data)
        return redirect(cost.get_absolute_url())


class ChangeCostView(DefaultView):
    """View to change a cost"""

    form_class = CostForm
    template_name = 'costs/change_cost.html'

    def get(self, request, pk):
        get_costs_service = GetCostsService(request.user)
        get_categories_service = GetCategoriesService(request.user)
        cost = get_costs_service.get_concrete(pk)
        form = self.form_class(instance=cost)
        user_categories = get_categories_service.get_all()
        set_form_categories(form, user_categories)
        return render(
            request, self.template_name, {'form': form, 'cost': cost}
        )

    def post(self, request, pk):
        get_costs_service = GetCostsService(request.user)
        get_categories_service = GetCategoriesService(request.user)
        self.cost = get_costs_service.get_concrete(pk)
        form = self.form_class(request.POST, instance=self.cost)
        user_categories = get_categories_service.get_all()
        set_form_categories(form, user_categories)
        if form.is_valid():
            return self.form_valid(request, form)

        return render(
            request, self.template_name, {'form': form, 'cost': self.cost}
        )

    def form_valid(self, request, form):
        form.cleaned_data.update({'cost': self.cost})
        cost = ChangeCostService.execute(form.cleaned_data)
        return redirect(cost.get_absolute_url())


class DeleteCostView(DeleteGenericView):
    """View to delete a cost"""

    template_name = 'costs/delete_cost.html'
    success_url = reverse_lazy('today_costs')
    context_object_name = 'cost'
    get_service_class = GetCostsService
    delete_service = DeleteCostService


class StatisticView(DefaultView):
    """View to return json with costs statistic"""

    def get(self, request, date):
        data = GetStatisticForTheMonthService.execute({
            'user': request.user,
            'date': date
        })
        return JsonResponse(data, safe=False)


class CostsStatisticPageView(StatisticPageGenericView):
    """View to render statistic with costs for the month"""

    template_name = 'costs/costs_statistic.html'
    command = GetCostsStatisticCommand


class CostStatisticForTheLastYear(DefaultView):
    """View to return json statistic with costs by months
    for the last year
    """

    def get(self, request, date):
        data = GetStatisticForTheYearService.execute({
            'user': request.user,
            'date': date
        })
        return JsonResponse(data, safe=False)
