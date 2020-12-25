import datetime
from typing import Optional

from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet, Model

import costs.services
import services.common as services_common
from .date import ContextDate, MonthContextDate


class BaseGenericListView(LoginRequiredMixin, View):
    """Base view for generic views that render list of model entries

    Attributes
    ----------
    model : Type[Model]
        Model that using to getting entries
    template_name : str
        Name of rendering template
    context_object_name : str
        Name of QuerySet with model entries in template

    """

    login_url = reverse_lazy('account_login')
    model = None
    template_name = ''
    context_object_name = 'object_list'

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not self.model:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `model` attribute"
            )
        if not self.template_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`template_name` attribute"
            )

        return super().dispatch(request, *args, **kwargs)


class DateGenericView(BaseGenericListView):
    """Base generic view to display entries for the date"""

    def get_queryset(self) -> QuerySet:
        """Return QuerySet with rendering model entries"""
        return services_common.get_for_the_date(
            self.model, self.request.user, self.date
        )

    def get_context_data(
            self, request: HttpRequest,
            date: Optional[datetime.date]) -> dict:
        """Return context for the template"""
        context_date = ContextDate(date)
        object_list = self.get_queryset()
        total_sum = services_common.get_total_sum(object_list)
        context = {
            self.context_object_name: object_list,
            'total_sum': total_sum,
            'date': context_date,
        }
        return context

    def get(self, request: HttpRequest,
            date: Optional[datetime.date] = None) -> HttpResponse:
        self.date = date
        context = self.get_context_data(request, date)
        return render(request, self.template_name, context)


class HistoryGenericView(BaseGenericListView):
    """Base generic view to display all entries"""

    def get_queryset(self) -> QuerySet:
        """Return QuerySet with model entries"""
        return services_common.get_all_user_entries(
            self.model, self.request.user
        )

    def get_context_data(self, request: HttpRequest) -> dict:
        """Return dict with context variables"""
        object_list = self.get_queryset()
        total_sum = services_common.get_total_sum(object_list)
        context = {
            self.context_object_name: object_list,
            'total_sum': total_sum
        }
        return context

    def get(self, request: HttpRequest) -> HttpResponse:
        context = self.get_context_data(request)
        return render(request, self.template_name, context)


class StatisticPageGenericView(BaseGenericListView):
    """Base generic view to display statistic page for the month"""

    def get_queryset(self) -> QuerySet:
        """Return QuerySet with model entries"""
        return services_common.get_for_the_month(
            self.model, self.request.user, self.date
        )

    def get_context_data(
            self, request: HttpRequest,
            date: Optional[datetime.date]) -> dict:
        """Return context for template"""
        context_date = MonthContextDate(date)
        object_list = self.get_queryset()
        total_sum = services_common.get_total_sum(object_list)
        profit = services_common.get_profit_for_the_month(request.user, date)
        average_costs = costs.services.get_average_costs_for_the_day(
            request.user
        )
        context = {
            self.context_object_name: object_list,
            'date': context_date,
            'total_sum': total_sum,
            'profit': profit,
            'average_costs': average_costs
        }
        return context

    def get(self, request: HttpRequest,
            date: Optional[datetime.date] = None) -> HttpResponse:
        self.date = date
        context = self.get_context_data(request, date)
        return render(request, self.template_name, context)


class GetUserObjectMixin:
    """
    Mixin that overrides the `get_object` method to return user object
    """

    def get_object(self) -> Model:
        pk = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(self.model, pk=pk, owner=self.request.user)
