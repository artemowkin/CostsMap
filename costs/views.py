from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import IntegrityError

from .forms import CategoryForm, CostForm
from .services.categories import CategoryService
from .services.costs import CostService
from .services.commands import GetCostsStatisticCommand
from incomes.services import IncomeService
from utils.views import (
    DateGenericView, HistoryGenericView, StatisticPageGenericView
)


class CategoryListView(LoginRequiredMixin, View):
    """View to render all user categories"""

    template_name = 'costs/category_list.html'
    context_object_name = 'categories'
    login_url = reverse_lazy('account_login')
    service = CategoryService()

    def get(self, request):
        categories = self.service.get_all(self.request.user)
        return render(
            request, self.template_name, {
                self.context_object_name: categories
            }
        )


class CostsByCategoryView(LoginRequiredMixin, View):
    """View to render all user category costs"""

    template_name = 'costs/costs_by_category.html'
    context_object_name = 'costs'
    login_url = reverse_lazy('account_login')
    service = CategoryService()
    cost_service = CostService()

    def get(self, request, pk):
        category = self.service.get_concrete(pk, request.user)
        costs = self.service.get_category_costs(category)
        total_sum = self.cost_service.get_total_sum(costs)
        return render(
            request, self.template_name, {
                self.context_object_name: costs,
                'category': category, 'total_sum': total_sum
            }
        )


class CreateCategoryView(LoginRequiredMixin, View):
    """View to create a new category"""

    form_class = CategoryForm
    template_name = 'costs/add_category.html'
    login_url = reverse_lazy('account_login')
    service = CategoryService()

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            category = self.service.create(form.cleaned_data, request.user)
            return redirect(category.get_absolute_url())

        return render(request, self.template_name, {'form': form})


class ChangeCategoryView(LoginRequiredMixin, View):
    """View to change a category"""

    form_class = CategoryForm
    template_name = 'costs/change_category.html'
    login_url = reverse_lazy('account_login')
    service = CategoryService()

    def get(self, request, pk):
        category = self.service.get_concrete(pk, request.user)
        form = self.form_class(instance=category)
        return render(
            request, self.template_name, {'form': form, 'category': category}
        )

    def post(self, request, pk):
        category = self.service.get_concrete(pk, request.user)
        form = self.form_class(request.POST, instance=category)
        if form.is_valid():
            try:
                category = self.service.change(category, form)
            except IntegrityError:
                form.add_error(
                    None, 'Category with the same title already exist'
                )
                category = self.service.get_concrete(pk, request.user)
            else:
                return redirect(category.get_absolute_url())

        return render(
            request, self.template_name, {'form': form, 'category': category}
        )


class DeleteCategoryView(LoginRequiredMixin, View):
    """View to delete a category"""

    template_name = 'costs/delete_category.html'
    success_url = reverse_lazy('category_list')
    login_url = reverse_lazy('account_login')
    service = CategoryService()

    def get(self, request, pk):
        category = self.service.get_concrete(pk, request.user)
        return render(request, self.template_name, {'category': category})

    def post(self, request, pk):
        category = self.service.get_concrete(pk, request.user)
        self.service.delete(category)
        return redirect(self.success_url)


class CostsForTheDateView(DateGenericView):
    """View to render costs for the date"""

    service = CostService()
    template_name = 'costs/costs.html'
    context_object_name = 'costs'


class CostsHistoryView(HistoryGenericView):
    """View to render all costs for all time."""

    service = CostService()
    template_name = 'costs/history_costs.html'
    context_object_name = 'costs'


class CreateCostView(LoginRequiredMixin, View):
    """View to create a new cost"""

    form_class = CostForm
    template_name = 'costs/add_cost.html'
    login_url = reverse_lazy('account_login')
    service = CostService()
    category_service = CategoryService()

    def get(self, request):
        form = self.form_class()
        self.category_service.set_form_user_categories(form, request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        self.category_service.set_form_user_categories(form, request.user)
        if form.is_valid():
            cost = self.service.create(form.cleaned_data, request.user)
            return redirect(cost.get_absolute_url())

        return render(request, self.template_name, {'form': form})


class ChangeCostView(LoginRequiredMixin, View):
    """View to change a cost"""

    service = CostService()
    form_class = CostForm
    template_name = 'costs/change_cost.html'
    login_url = reverse_lazy('account_login')

    def get(self, request, pk):
        cost = self.service.get_concrete(pk, request.user)
        form = self.form_class(instance=cost)
        return render(
            request, self.template_name, {'form': form, 'cost': cost}
        )

    def post(self, request, pk):
        cost = self.service.get_concrete(pk, request.user)
        form = self.form_class(request.POST, instance=cost)
        if form.is_valid():
            cost = self.service.change(cost, form)
            return redirect(cost.get_absolute_url())

        return render(
            request, self.template_name, {'form': form, 'cost': cost}
        )


class DeleteCostView(LoginRequiredMixin, View):
    """View to delete a cost"""

    template_name = 'costs/delete_cost.html'
    success_url = reverse_lazy('today_costs')
    login_url = reverse_lazy('account_login')
    service = CostService()

    def get(self, request, pk):
        cost = self.service.get_concrete(pk, request.user)
        return render(request, self.template_name, {'cost': cost})

    def post(self, request, pk):
        cost = self.service.get_concrete(pk, request.user)
        self.service.delete(cost)
        return redirect(self.success_url)


class StatisticView(LoginRequiredMixin, View):
    """View to return json with costs statistic"""

    login_url = reverse_lazy('account_login')
    service = CostService()

    def get(self, request, date):
        data = self.service.get_statistic_for_the_month(request.user, date)
        return JsonResponse(data, safe=False)


class CostsStatisticPageView(StatisticPageGenericView):
    """View to render statistic with costs for the month"""

    template_name = 'costs/costs_statistic.html'
    cost_service = CostService()
    income_service = IncomeService()
    command = GetCostsStatisticCommand


class CostStatisticForTheLastYear(LoginRequiredMixin, View):
    """
    View to return json statistic with costs by months
    for the last year
    """

    login_url = reverse_lazy('account_login')
    service = CostService()

    def get(self, request, date):
        data = self.service.get_statistic_for_the_year(request.user, date)
        return JsonResponse(data, safe=False)
