from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy

from ..forms import CostForm
from ..models import Cost, Category
from ..services.commands import GetCostsStatisticCommand
import costs.services as cost_services
import costs.services.categories as category_services
import services.common as common_services
from utils.views import (
    DateGenericView, HistoryGenericView, StatisticPageGenericView,
    DeleteGenericView, DefaultView
)


class CostsForTheDateView(DateGenericView):
    """View to render costs for the date"""

    template_name = 'costs/costs.html'
    context_object_name = 'costs'
    model = Cost

    def get_total_sum(self, costs):
        return cost_services.get_total_sum(costs)


class CostsHistoryView(HistoryGenericView):
    """View to render all costs for all time."""

    template_name = 'costs/history_costs.html'
    context_object_name = 'costs'
    model = Cost

    def get_total_sum(self, costs):
        return cost_services.get_total_sum(costs)


class CreateCostView(DefaultView):
    """View to create a new cost"""

    model = Cost
    category_model = Category
    form_class = CostForm
    template_name = 'costs/add_cost.html'

    def get(self, request):
        form = self.form_class()
        user_categories = common_services.get_all_user_entries(
            self.category_model, request.user
        )
        category_services.set_form_categories(form, user_categories)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        user_categories = common_services.get_all_user_entries(
            self.category_model, request.user
        )
        category_services.set_form_categories(form, user_categories)
        if form.is_valid():
            form.cleaned_data.update({'owner': request.user})
            cost = common_services.create_entry(
                self.model, form.cleaned_data
            )
            return redirect(cost.get_absolute_url())

        return render(request, self.template_name, {'form': form})


class ChangeCostView(DefaultView):
    """View to change a cost"""

    model = Cost
    category_model = Category
    form_class = CostForm
    template_name = 'costs/change_cost.html'

    def get(self, request, pk):
        cost = common_services.get_concrete_user_entry(
            self.model, pk, request.user
        )
        form = self.form_class(instance=cost)
        user_categories = common_services.get_all_user_entries(
            self.category_model, request.user
        )
        category_services.set_form_categories(form, user_categories)
        return render(
            request, self.template_name, {'form': form, 'cost': cost}
        )

    def post(self, request, pk):
        cost = common_services.get_concrete_user_entry(
            self.model, pk, request.user
        )
        form = self.form_class(request.POST, instance=cost)
        user_categories = common_services.get_all_user_entries(
            self.category_model, request.user
        )
        category_services.set_form_categories(form, user_categories)
        if form.is_valid():
            common_services.change_entry(cost, form.cleaned_data)
            return redirect(cost.get_absolute_url())

        return render(
            request, self.template_name, {'form': form, 'cost': cost}
        )


class DeleteCostView(DeleteGenericView):
    """View to delete a cost"""

    model = Cost
    template_name = 'costs/delete_cost.html'
    success_url = reverse_lazy('today_costs')
    context_object_name = 'cost'


class StatisticView(DefaultView):
    """View to return json with costs statistic"""

    def get(self, request, date):
        data = cost_services.GetStatisticForTheMonthService.execute({
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
        data = cost_services.GetStatisticForTheYearService.execute({
            'user': request.user,
            'date': date
        })
        return JsonResponse(data, safe=False)
