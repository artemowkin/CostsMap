"""Module with views utilities"""

import datetime

from django.views import View
from django.forms import Form
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import Http404
from django.conf import settings
from django.urls import reverse

from utils.date import ContextDate, MonthContextDate


class BaseView(View):

    """Base view class with exceptions handling

    Attributes
    ----------
    error_template : str
        Template with an error message to the user

    """

    error_template = 'errors/something_strange.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Handle exceptions. Render the error_template if
        get strange exception
        """
        try:
            return super().dispatch(request, *args, **kwargs)
        except (Http404, PermissionDenied, ImproperlyConfigured):
            raise
        except Exception:
            if settings.DEBUG:
                raise

            return render(request, 'errors/something_strange.html')


class RenderAuthorizedView(LoginRequiredMixin, BaseView):

    """Abstract view to render template with user authentication check

    Attributes
    ----------
    login_url : str
        The url the user will be redirected if not authenticated

    service : Service
        The service the view works with

    template_name : str
        The name of the template used for the response

    """

    login_url = 'account_login'
    service = None
    template_name = ''

    def dispatch(self, request, *args, **kwargs):
        """Check if service and template_name are identified"""
        if not (self.service and self.template_name):
            raise NotImplementedError(
                f"{self.__class__.__name__} must have `service` and "
                "`template_name` attributes"
            )

        return super().dispatch(request, *args, **kwargs)


class APIAuthorizedView(LoginRequiredMixin, BaseView):

    """Abstract view to return JSON with user authentication check

    Attributes
    ----------
    service : Service
        The service the view works with

    """

    service = None

    def dispatch(self, request, *args, **kwargs):
        """Check if service is identified"""
        if not self.service:
            raise NotImplementedError(
                f"{self.__class__.__name__} must have a `service` attribute"
            )

        return super().dispatch(request, *args, **kwargs)


class CreateView(RenderAuthorizedView):

    """Abstract view to create an instance"""

    def get(self, request):
        """Return create form"""
        form = self.service.get_create_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Create an instance. If POST data is correct then redirect to
        absolute url of instance. Else return form with errors
        """
        response = self.service.create(
            form_data=request.POST, owner=request.user
        )
        if isinstance(response, Form):
            return render(request, self.template_name, {'form': response})

        return redirect(response.get_absolute_url())


class ChangeView(RenderAuthorizedView):

    """Abstract view to change an instance

    Attributes
    ----------
    context_object_name : str
        Name of context model's instance. `object` by default

    """

    context_object_name = 'object'

    def get(self, request, pk):
        """
        Return form with model's instance data and model's instance itself
        """
        form = self.service.get_change_form(pk=pk, owner=request.user)
        instance = self.service.get_concrete(pk=pk, owner=request.user)
        context = {'form': form, self.context_object_name: instance}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        """
        Change an instance. If form data is valid then redirect
        to absolute url of the instance. Else return form with errors and
        the instance itself
        """
        response = self.service.change(
            form_data=request.POST, pk=pk, owner=request.user
        )
        if isinstance(response, Form):
            instance = self.service.get_concrete(pk=pk, owner=request.user)
            context = {'form': response, self.context_object_name: instance}
            return render(request, self.template_name, context)

        return redirect(response.get_absolute_url())


class DeleteView(RenderAuthorizedView):

    """Abstract view to delete an instance

    Attributes
    ----------
    context_object_name : str
        Name of context model's instance. By default `object`

    """

    context_object_name = 'object'

    def get(self, request, pk):
        """Return model's instance"""
        instance = self.service.get_concrete(pk=pk, owner=request.user)
        context = {self.context_object_name: instance}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        """Delete the instance and redirect to today costs page"""
        self.service.delete(pk=pk, owner=request.user)
        return redirect(reverse('today_costs'))


class DateView(RenderAuthorizedView):

    """Abstract view to return entries for the date

    Attributes
    ----------
    service : Service
        The service the view works with

    template_name : str
        Template to display entries for the date

    context_object_name : str
        Name of context object. By default `object`


    Methods
    -------
    get_context(request, date)
        Return context for the template

    """

    service = None
    template_name = 'costs/costs.html'
    context_object_name = 'object_list'

    def dispatch(self, request, *args, **kwargs):
        """Check if service and template_name are identified"""
        if not (self.service and self.template_name):
            raise NotImplementedError(
                f"{self.__class__.__name__} must have `service` and "
                "`template_name` attributes"
            )

        return super().dispatch(request, *args, **kwargs)

    def get_context(self, request, date):
        """Return context for the template"""
        context_date = ContextDate(date)
        context = {
            self.context_object_name: self.entries,
            'total_sum': self.total_sum,
            'date': context_date.date,
            'previous_date': context_date.previous_day,
            'next_date': context_date.next_day
        }
        return context

    def get(self, request, date=None):
        """Return entries for the date"""
        if not date:
            date = datetime.date.today()

        self.entries = self.service.get_for_the_date(
            owner=request.user, date=date
        )
        self.total_sum = self.service.get_total_sum(self.entries)

        context = self.get_context(request, date)
        return render(request, self.template_name, context)


# TODO: Move it in history app
class HistoryView(RenderAuthorizedView):

    """Abstract view to return all entries for all time.

    Attributes
    ----------
    context_object_name : str
        Name of entry in template

    """

    context_object_name = 'object_list'

    def get(self, request):
        """Return all entries for all time"""
        all_entries = self.service.get_all(owner=request.user)
        total_sum = self.service.get_total_sum(all_entries)

        context = {
            self.context_object_name: all_entries,
            'total_sum': total_sum
        }
        return render(request, self.template_name, context)


class StatisticPageView(RenderAuthorizedView):

    """Abstract view to return statistic with entries fot the month.

    Attributes
    ----------
    context_object_name : str
        Entry name in template

    costs_service : Service
        Cost's service to calculate a profit

    """

    context_object_name = 'object'
    cost_service = None

    def get_context(self, request, date):
        """Return context for template"""
        context_date = MonthContextDate(date)
        context = {
            self.context_object_name: self.entries_for_the_month,
            'date': context_date.date,
            'previous_date': context_date.previous_month,
            'next_date': context_date.next_month,
            'total_sum': self.total_sum,
            'profit': self.profit,
            'average_costs': self.average_costs,
        }
        return context

    def get(self, request, date=None):
        """Render template with entries for the month in date"""
        self.entries_for_the_month = self.service.get_for_the_month(
            owner=request.user, date=date
        )
        self.total_sum = self.service.get_total_sum(
            self.entries_for_the_month
        )
        self.profit = self.cost_service.get_profit_for_the_month(
            request.user, date=date
        )
        self.average_costs = self.cost_service.get_average_costs_for_the_day(
            request.user
        )

        context = self.get_context(request, date)
        return render(request, self.template_name, context)

