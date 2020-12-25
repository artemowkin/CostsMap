import datetime
from uuid import UUID

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.forms import Form

from .models import Category, Cost
from .forms import CategoryForm, CostForm
from . import services
import services.common as services_common
from utils.views import (
    DateGenericView, HistoryGenericView, StatisticPageGenericView,
    GetUserObjectMixin
)


class CategoryListView(LoginRequiredMixin, View):
    """View to render all user categories

    Attributes
    ----------
    template_name : str
        Template to display categories
    context_object_name : str
        Name of categories queryset in context

    """

    template_name = 'costs/category_list.html'
    context_object_name = 'categories'
    login_url = reverse_lazy('account_login')

    def get(self, request: HttpRequest) -> HttpResponse:
        categories = services_common.get_all_user_entries(
            Category, self.request.user
        )
        return render(
            request, self.template_name, {
                self.context_object_name: categories
            }
        )


class CostsByCategoryView(LoginRequiredMixin, View):
    """View to render all user category costs

    Attributes
    ----------
    template_name : str
        Template to display costs
    context_object_name : str
        Name of costs queryset in context

    """

    template_name = 'costs/costs_by_category.html'
    context_object_name = 'costs'
    login_url = reverse_lazy('account_login')

    def get(self, request: HttpRequest, pk: UUID) -> HttpResponse:
        category, costs = services.get_category_costs(pk, request.user)
        total_sum = services_common.get_total_sum(costs)
        return render(
            request, self.template_name, {
                self.context_object_name: costs,
                'category': category, 'total_sum': total_sum
            }
        )


class CreateCategoryView(LoginRequiredMixin, CreateView):
    """View to create a new category"""

    model = Category
    form_class = CategoryForm
    template_name = 'costs/add_category.html'
    login_url = reverse_lazy('account_login')

    def form_valid(self, form: Form) -> HttpResponse:
        form.instance.owner = self.request.user
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(
                None, 'Category with the same title already exist'
            )
            return super().form_invalid(form)


class ChangeCategoryView(LoginRequiredMixin, GetUserObjectMixin, UpdateView):
    """View to change a category"""

    model = Category
    form_class = CategoryForm
    template_name = 'costs/change_category.html'
    context_object_name = 'category'
    login_url = reverse_lazy('account_login')


class DeleteCategoryView(LoginRequiredMixin, GetUserObjectMixin, DeleteView):
    """View to delete a category"""

    model = Category
    template_name = 'costs/delete_category.html'
    context_object_name = 'category'
    success_url = reverse_lazy('category_list')
    login_url = reverse_lazy('account_login')


class CostsForTheDateView(DateGenericView):
    """View to render costs for the date

    Attributes
    ----------
    model : Type[Model]
        Cost model
    template_name : str
        Template to display costs for the date
    context_object_name : str
        Name of costs in template

    """

    model = Cost
    template_name = 'costs/costs.html'
    context_object_name = 'costs'


class CostsHistoryView(HistoryGenericView):
    """View to render all costs for all time.

    Attributes
    ----------
    template_name : str
        Template to display history of costs
    context_object_name : str
        Name of costs in template

    """

    model = Cost
    template_name = 'costs/history_costs.html'
    context_object_name = 'costs'


class UserCategoriesInFormMixin:
    """Mixin that setting user categories in cost form"""

    def get_form(self, *args, **kwargs) -> Form:
        form = super().get_form(*args, **kwargs)
        services.set_form_owner_categories(form, self.request.user)
        return form


class CreateCostView(
        LoginRequiredMixin, UserCategoriesInFormMixin, CreateView):
    """View to create a new cost"""

    model = Cost
    form_class = CostForm
    template_name = 'costs/add_cost.html'
    login_url = reverse_lazy('account_login')

    def form_valid(self, form: Form) -> HttpResponse:
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ChangeCostView(
        LoginRequiredMixin, UserCategoriesInFormMixin, GetUserObjectMixin,
        UpdateView):
    """View to change a cost"""

    model = Cost
    form_class = CostForm
    template_name = 'costs/change_cost.html'
    context_object_name = 'cost'
    login_url = reverse_lazy('account_login')


class DeleteCostView(LoginRequiredMixin, GetUserObjectMixin, DeleteView):
    """View to delete a cost"""

    model = Cost
    template_name = 'costs/delete_cost.html'
    context_object_name = 'cost'
    success_url = reverse_lazy('today_costs')
    login_url = reverse_lazy('account_login')


class StatisticView(LoginRequiredMixin, View):
    """View to return json with costs statistic"""

    login_url = reverse_lazy('account_login')

    def get(self, request: HttpRequest, date: datetime.date) -> JsonResponse:
        data = services.get_costs_statistic_for_the_month(
            owner=request.user, date=date
        )
        return JsonResponse(data, safe=False)


class CostsStatisticPageView(StatisticPageGenericView):
    """View to render statistic with costs for the month"""

    model = Cost
    template_name = 'costs/costs_statistic.html'
    context_object_name = 'costs'


class CostStatisticForTheLastYear(LoginRequiredMixin, View):
    """
    View to return json statistic with costs by months
    for the last year
    """

    login_url = reverse_lazy('account_login')

    def get(self, request: HttpRequest, date: datetime.date) -> JsonResponse:
        data = services.get_costs_statistic_for_the_year(
            request.user, date
        )
        return JsonResponse(data, safe=False)
