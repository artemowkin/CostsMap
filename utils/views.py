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


class RenderView(DefaultView):
    """Default view with template_name attribute"""

    template_name = ''

    def __init__(self, *args, **kwargs):
        if not self.template_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`template_name` attribute"
            )

        super().__init__(*args, **kwargs)


class DateGenericView(RenderView):
    """Base generic view to display entries for the date"""

    date_service = None
    total_sum_service = None
    context_object_name = 'object_list'

    def __init__(self, *args, **kwargs):
        if not self.date_service:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`date_service` attribute"
            )
        if not self.total_sum_service:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`total_sum_service` attribute"
            )

        super().__init__(*args, **kwargs)

    def get(self, request, date=None):
        context_date = ContextDate(date)
        date_entries = self.date_service.get_for_the_date(
            request.user, date
        )
        total_sum = self.total_sum_service.execute(date_entries)
        context = {
            self.context_object_name: date_entries,
            'total_sum': total_sum,
            'date': context_date,
        }
        return render(request, self.template_name, context)


class HistoryGenericView(RenderView):
    """Base generic view to display all entries"""

    context_object_name = 'object_list'
    get_service = None
    total_sum_service = None

    def __init__(self, *args, **kwargs):
        if not self.get_service:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`get_service` attribute"
            )
        if not self.total_sum_service:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`total_sum_service` attribute"
            )

        super().__init__(*args, **kwargs)

    def get(self, request):
        all_entries = self.get_service.get_all(request.user)
        total_sum = self.total_sum_service.execute(all_entries)
        context = {
            self.context_object_name: all_entries,
            'total_sum': total_sum
        }
        return render(request, self.template_name, context)


class StatisticPageGenericView(View):
    """Generic view to render statistic page"""

    template_name = ''
    command = None

    def __init__(self, *args, **kwargs):
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
            request.user, date
        )
        statistic = command.execute()
        return render(request, self.template_name, statistic)


class DeleteGenericView(RenderView):
    """Base view to delete entries"""

    success_url = '/'
    context_object_name = 'object'
    get_service = None
    delete_service = None

    def __init__(self, *args, **kwargs):
        if not self.get_service:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `get_service` attribute"
            )
        if not self.delete_service:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`delete_service` attribute"
            )

        super().__init__(*args, **kwargs)

    def get(self, request, pk):
        entry = self.get_service.get_concrete(pk, request.user)
        return render(
            request, self.template_name, {self.context_object_name: entry}
        )

    def post(self, request, pk):
        entry = self.get_service.get_concrete(pk, request.user)
        self.delete_service.execute({self.context_object_name: entry})
        return redirect(self.success_url)
