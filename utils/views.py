import logging

from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response


logger = logging.getLogger('filelogger')


class DefaultView(LoginRequiredMixin, APIView):
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
        if not self.command:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `command` attribute"
            )

        super().__init__(*args, **kwargs)


class DateGenericView(CommandView):
    """Base generic view to display entries for the date"""

    def get(self, request, date=None):
        command = self.command(request.user, date)
        data = command.execute()
        return Response(data)


class HistoryGenericView(CommandView):
    """Base generic view to display all entries"""

    def get(self, request):
        command = self.command(request.user)
        data = command.execute()
        return Response(data)


class StatisticPageGenericView(CommandView):
    """Generic view to render statistic page"""

    def get(self, request, date=None):
        command = self.command(request.user, date)
        statistic = command.execute()
        return Response(statistic)


class DeleteGenericView(DefaultView):
    """Base view to delete entries"""

    object_name = 'object'
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

    def post(self, request, pk):
        entry = self.get_service.get_concrete(pk, request.user)
        self.delete_service.execute({self.object_name: entry})
        return Response({'status': 'ok'})
