from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured

from .date import ContextDate


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
    service = None
    template_name = ''
    context_object_name = 'object_list'

    def dispatch(self, request, *args, **kwargs):
        if not self.service:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `service` attribute"
            )
        if not self.template_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`template_name` attribute"
            )

        return super().dispatch(request, *args, **kwargs)


class DateGenericView(BaseGenericListView):
    """Base generic view to display entries for the date"""

    def get_context_data(self, request, date=None) -> dict:
        """Return context for the template"""
        context_date = ContextDate(date)
        date_entries = self.service.get_for_the_date(request.user, date)
        total_sum = self.service.get_total_sum(date_entries)
        context = {
            self.context_object_name: date_entries,
            'total_sum': total_sum,
            'date': context_date,
        }
        return context

    def get(self, request, date=None):
        context = self.get_context_data(request, date)
        return render(request, self.template_name, context)


class HistoryGenericView(BaseGenericListView):
    """Base generic view to display all entries"""

    def get_context_data(self, request) -> dict:
        """Return dict with context variables"""
        all_entries = self.service.get_all(request.user)
        total_sum = self.service.get_total_sum(all_entries)
        context = {
            self.context_object_name: all_entries,
            'total_sum': total_sum
        }
        return context

    def get(self, request):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)


class StatisticPageGenericView(View):
    """Generic view to render statistic page"""

    template_name = ''
    cost_service = None
    income_service = None
    command = None

    def dispatch(self, request, *args, **kwargs):
        if not self.cost_service:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`cost_service` attribute"
            )
        if not self.income_service:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`income_service` attribute"
            )
        if not self.command:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `command` attribute"
            )
        if not self.template_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`template_name` attribute"
            )

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, date=None):
        command = self.command(
            self.cost_service, self.income_service, request.user, date
        )
        statistic = command.execute()
        return render(request, self.template_name, statistic)
