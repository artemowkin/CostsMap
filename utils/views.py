import logging

from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404


logger = logging.getLogger('filelogger')


class DefaultView(LoginRequiredMixin, View):
    """Base view for all views. Handle exceptions and logs them"""

    login_url = reverse_lazy('account_login')

    def dispatch(self, request, *args, **kwargs):
        try:
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


class CommandView(DefaultView):
    """Default view using commands"""

    template_name = ''
    command = None

    def __init__(self, *args, **kwargs):
        if not self.template_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`template_name` attribute"
            )
        if not self.command:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `command` attribute"
            )

        super().__init__(*args, **kwargs)


class DateGenericView(CommandView):
    """Base generic view to display entries for the date"""

    def get(self, request, date=None):
        command = self.command(request.user, date)
        context = command.execute()
        return render(request, self.template_name, context)


class HistoryGenericView(CommandView):
    """Base generic view to display all entries"""

    def get(self, request):
        command = self.command(request.user)
        context = command.execute()
        return render(request, self.template_name, context)


class StatisticPageGenericView(CommandView):
    """Generic view to render statistic page"""

    def get(self, request, date=None):
        command = self.command(request.user, date)
        statistic = command.execute()
        return render(request, self.template_name, statistic)


class DeleteGenericView(DefaultView):
    """Base view to delete entries"""

    template_name = ''
    success_url = '/'
    context_object_name = 'object'
    get_service = None
    delete_service = None

    def __init__(self, *args, **kwargs):
        if not self.template_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`template_name` attribute"
            )
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
