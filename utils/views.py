import logging

from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404

from .date import ContextDate


logger = logging.getLogger('filelogger')


class DefaultView(LoginRequiredMixin, View):
    """Base view for all views. Handle exceptions and logs them"""

    login_url = reverse_lazy('account_login')

    def dispatch(self, request, *args, **kwargs):
        try:
            logger.info(
                f"{request.user} requesting {request.get_full_path()} "
                f"with method {request.method}, GET: {request.GET},"
                f" POST: {request.POST}, FILES: {request.FILES}, "
                f"cookies: {request.COOKIES}"
            )
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            logger.error(f"404 HTTP Not Found on {request.get_full_path()}")
            raise
        except Exception as e:
            logger.exception(
                f"{e.__class__.__name__} exception on "
                "{request.get_full_path()}"
            )
            raise


class BaseServicesView(DefaultView):
    """Base view for all views working with services

    Attributes
    ----------
    service
        Service view works with
    template_name : str
        Name of rendering template
    context_object_name : str
        Name of object rendering on page. By default it's `object`

    """

    service = None
    template_name = ''
    context_object_name = 'object'

    def __init__(self, *args, **kwargs):
        if not self.service:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `service` attribute"
            )
        if not self.template_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`template_name` attribute"
            )

        super().__init__(*args, **kwargs)


class DateGenericView(BaseServicesView):
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


class HistoryGenericView(BaseServicesView):
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

    def __init__(self, *args, **kwargs):
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

        super().__init__(*args, **kwargs)

    def get(self, request, date=None):
        command = self.command(
            self.cost_service, self.income_service, request.user, date
        )
        statistic = command.execute()
        return render(request, self.template_name, statistic)


class BaseCRUDView(BaseServicesView):
    """Base view for CRUD views"""

    form_class = None

    def __init__(self, *args, **kwargs):
        if not self.form_class:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `form_class` attribute"
            )

        super().__init__(*args, **kwargs)


class CreateGenericView(BaseCRUDView):
    """Base view to create entries"""

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            entry = self.service.create(form.cleaned_data, request.user)
            return redirect(entry.get_absolute_url())

        return render(request, self.template_name, {'form': form})


class ChangeGenericView(BaseCRUDView):
    """Base view to change entries"""

    def get(self, request, pk):
        entry = self.service.get_concrete(pk, request.user)
        form = self.form_class(instance=entry)
        return render(
            request, self.template_name, {
                'form': form, self.context_object_name: entry
            }
        )

    def post(self, request, pk):
        entry = self.service.get_concrete(pk, request.user)
        form = self.form_class(request.POST, instance=entry)
        if form.is_valid():
            entry = self.service.change(entry, form)
            return redirect(entry.get_absolute_url())

        return render(
            request, self.template_name, {
                'form': form, self.context_object_name: cost
            }
        )


class DeleteGenericView(BaseServicesView):
    """Base view to delete entries"""

    success_url = '/'

    def get(self, request, pk):
        entry = self.service.get_concrete(pk, request.user)
        return render(
            request, self.template_name, {self.context_object_name: entry}
        )

    def post(self, request, pk):
        entry = self.service.get_concrete(pk, request.user)
        self.service.delete(entry)
        return redirect(self.success_url)
