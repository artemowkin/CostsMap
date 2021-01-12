import logging

from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404

from .date import ContextDate
import services.common as common_services


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


class DateGenericView(DefaultView):
    """Base generic view to display entries for the date"""

    model = None

    def __init__(self, *args, **kwargs):
        if not self.model:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `model` attribute"
            )

        super().__init__(*args, **kwargs)

    def get_context_data(self, request, date=None) -> dict:
        """Return context for the template"""
        context_date = ContextDate(date)
        date_entries = common_services.get_for_the_date(
            self.model, request.user, date
        )
        total_sum = self.get_total_sum(date_entries)
        context = {
            self.context_object_name: date_entries,
            'total_sum': total_sum,
            'date': context_date,
        }
        return context

    def get(self, request, date=None):
        context = self.get_context_data(request, date)
        return render(request, self.template_name, context)


class HistoryGenericView(DefaultView):
    """Base generic view to display all entries"""

    model = None

    def __init__(self, *args, **kwargs):
        if not self.model:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `model` attribute"
            )
        if not self.get_total_sum:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`get_total_sum` attribute"
            )

        super().__init__(*args, **kwargs)

    def get_context_data(self, request) -> dict:
        """Return dict with context variables"""
        all_entries = common_services.get_all_user_entries(
            self.model, request.user
        )
        total_sum = self.get_total_sum(all_entries)
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


class CreateGenericView(DefaultView):
    """Base view to create entries"""

    form_class = None
    template_name = ''
    model = None

    def __init__(self, *args, **kwargs):
        if not self.form_class:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `form_class` attribute"
            )
        if not self.template_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`template_name` attribute"
            )
        if not self.model:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `model` attribute"
            )

        super().__init__(*args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        form.cleaned_data.update({'owner': self.request.user})
        try:
            entry = common_services.create_entry(
                self.model, form.cleaned_data
            )
            return redirect(entry.get_absolute_url())
        except IntegrityError:
            form.add_error(
                None,
                f"The same {self.model._meta.verbose_name} already exists"
            )
            return self.form_invalid(form)

    def form_invalid(self, form):
        return render(request, self.template_name, {'form': form})


class ChangeGenericView(DefaultView):
    """Base view to change entries"""

    context_object_name = 'object'

    def get(self, request, pk):
        self.entry = common_services.get_concrete_user_entry(
            self.model, pk, request.user
        )
        form = self.form_class(instance=self.entry)
        return self._render_page(form)

    def post(self, request, pk):
        self.entry = common_services.get_concrete_user_entry(
            self.model, pk, request.user
        )
        form = self.form_class(request.POST, instance=self.entry)
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        try:
            common_services.change_entry(self.entry, form.cleaned_data)
            return redirect(self.entry.get_absolute_url())
        except IntegrityError:
            form.add_error(
                None,
                f"The same {self.model._meta.verbose_name} already exists"
            )
            self.entry = common_services.get_concrete_user_entry(
                self.model, self.entry.pk, self.request.user
            )
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self._render_page(form)

    def _render_page(self, form):
        return render(
            self.request, self.template_name, {
                'form': form, self.context_object_name: self.entry
            }
        )


class DeleteGenericView(DefaultView):
    """Base view to delete entries"""

    success_url = '/'

    def get(self, request, pk):
        entry = common_services.get_concrete_user_entry(
            self.model, pk, request.user
        )
        return render(
            request, self.template_name, {self.context_object_name: entry}
        )

    def post(self, request, pk):
        entry = common_services.get_concrete_user_entry(
            self.model, pk, request.user
        )
        common_services.delete_entry(entry)
        return redirect(self.success_url)
