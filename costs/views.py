"""Modules with views for costs"""

import datetime

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import Form
from django.urls import reverse
from django.http import JsonResponse
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import Http404
from django.conf import settings

from .services.costs import CostService
from .services.categories import CategoryService
from .services.incomes import IncomeService
from .templates import ContextDate


class BaseView(View):

    """
    Base view class with exceptions handling. Has following attributes:

        error_template -- template with an error message to the user

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

    """
    Abstract view with user authentication check and required
    `service` and `template_name` attributes. Has following attributes:

        login_url -- the url the user will be redirected
        if not authenticated

        service -- the service the view works with

        template_name -- the name of the template used for the response

    """

    login_url = 'account_login'
    service = None
    template_name = ''

    def dispatch(self, request, *args, **kwargs):
        """Check if service and template_name are identified"""
        if not (self.service and self.template_name):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `service` and "
                "`template_name` attributes"
            )

        return super().dispatch(request, *args, **kwargs)


class APIAuthorizedView(LoginRequiredMixin, BaseView):

    """
    Abstract view with user authentication check and required
    `service` attribute. Has following attributes:

        service -- the service the view works with

    """

    service = None

    def dispatch(self, request, *args, **kwargs):
        """Check if service is identified"""
        if not self.service:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have a `service` attribute"
            )

        return super().dispatch(request, *args, **kwargs)


class DateView(RenderAuthorizedView):

    """
    Abstract view to return entries for the date. Has following attributes:

        service -- the service the view works with

        template_name -- template to display entries for the date

        context_object_name -- name of context object. By default `object`

    """

    service = CostService()
    template_name = 'costs/costs.html'
    context_object_name = 'object_list'

    def get(self, request, date=None):
        """Return costs for the date"""
        if not date:
            date = datetime.date.today().isoformat()

        entries = self.service.get_for_the_date(
            owner=request.user, date=date
        )
        total_sum = self.service.get_total_sum(entries)

        context_date = ContextDate(date)
        context = {
            self.context_object_name: entries,
            'total_sum': total_sum,
            'date': context_date.date,
            'previous_date': context_date.previous_day,
            'next_date': context_date.next_day
        }
        return render(request, self.template_name, context)


class CostsForTheDateView(DateView):

    """
    View to return costs for the date. Has following attributes:

        service -- cost's service

        template_name -- template to display costs for the date

        context_object_name -- name of costs in template

    """

    service = CostService()
    template_name = 'costs/costs.html'
    context_object_name = 'costs'


class IncomesForTheDateView(DateView):

    """
    View to return incomes for the date. Has following attributes:

        service -- income's service

        template_name -- template to display income's for the date

        context_object_name -- name of incomes in template

    """

    service = IncomeService()
    template_name = 'costs/incomes.html'
    context_object_name = 'incomes'


class HistoryView(RenderAuthorizedView):

    """
    Abstract view to return all entries for all time.
    Has following attributes:

        context_object_name -- name of entry in template

    """

    context_object_name = 'object_list'

    def get(self, request):
        """Return all the costs for all time"""
        all_entries = self.service.get_all(owner=request.user)
        total_sum = self.service.get_total_sum(all_entries)

        context = {
            self.context_object_name: all_entries,
            'total_sum': total_sum
        }
        return render(request, self.template_name, context)


class CostsHistoryView(HistoryView):

    """
    View to return all costs for all time.
    Has following attributes:

        service -- cost's service

        template_name -- template to display history of costs

        context_object_name -- name of costs in template

    """

    service = CostService()
    template_name = 'costs/history_costs.html'
    context_object_name = 'costs'


class IncomesHistoryView(HistoryView):

    """
    View to return all incomes for all time.
    Has following attributes:

        service -- income's service

        template_name -- template to display history of incomes

        context_object_name -- name of incomes in template

    """

    service = IncomeService()
    template_name = 'costs/history_incomes.html'
    context_object_name = 'incomes'


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

    """
    Abstract view to change an instance. Has following attribute:

        context_object_name -- name of context model's instance. `object`
        by default

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

    """
    Abstract view to delete an instance. Has following attributes:

        context_object_name -- name of context model's instance.
        By default `object`

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


class CreateCostView(CreateView):

    """
    View to create a new cost. Has following attributes:

        service -- cost's service

        template_name -- template with form to create a cost

    """

    service = CostService()
    template_name = 'costs/add_cost.html'

    def get(self, request):
        """Return create cost form"""
        form = self.service.get_create_form(owner=request.user)
        return render(request, self.template_name, {'form': form})


class CreateIncomeView(CreateView):

    """
    View to create a new income. Has following attributes:

        service -- income's service

        template_name -- template with form to create an incomr

    """

    service = IncomeService()
    template_name = 'costs/add_income.html'


class ChangeCostView(ChangeView):

    """
    View to change a cost. Has following attributes:

        service -- cost's service

        template_name -- template with form to change a cost

        context_object_name -- name of cost object in template

    """

    service = CostService()
    template_name = 'costs/change_cost.html'
    context_object_name = 'cost'


class ChangeIncomeView(ChangeView):

    """
    View to change an income. Has following attributes:

        service -- income's service

        template_name -- template with form to change an income

        context_object_name -- name of income object in template

    """

    service = IncomeService()
    template_name = 'costs/change_income.html'
    context_object_name = 'income'


class DeleteCostView(DeleteView):

    """
    View to delete a cost. Has following attributes:

        service -- cost's service

        template_name -- template with confirmation form to delete
        an instance

        context_object_name -- name of cost object in template

    """

    service = CostService()
    template_name = 'costs/delete_cost.html'
    context_object_name = 'cost'


class DeleteIncomeView(DeleteView):

    """
    View to delete an income. Has following attributes:

        service -- income's service

        template_name -- template with form to delete an income

        context_object_name -- name of income object in template

    """

    service = IncomeService()
    template_name = 'costs/delete_income.html'
    context_object_name = 'income'


class CategoryListView(RenderAuthorizedView):

    """
    View to return all categories. Has following attributes:

        service -- category's service

        template_name -- template to display all categories

    """

    service = CategoryService()
    template_name = 'costs/category_list.html'

    def get(self, request):
        """Return categories list"""
        categories = self.service.get_all(owner=request.user)
        context = {'categories': categories}
        return render(request, self.template_name, context)


class CreateCategoryView(CreateView):

    """
    View to create a new category. Has following attributes:

        service -- category's service

        template_name -- template with form to create a new category

    """

    service = CategoryService()
    template_name = 'costs/add_category.html'


class ChangeCategoryView(ChangeView):

    """
    View to change a category. Has followgin attributes:

        service -- category's service

        template_name -- template with form to change a category

        context_object_name -- name of category object in template

    """

    service = CategoryService()
    template_name = 'costs/change_category.html'
    context_object_name = 'category'


class DeleteCategoryView(DeleteView):

    """
    View to delete a category. Has following attributes:

        service -- category's service

        template_name -- template with form to delete a category

        context_object_name -- name of category object in template

    """

    service = CategoryService()
    template_name = 'costs/delete_category.html'
    context_object_name = 'category'


class StatisticView(APIAuthorizedView):

    """
    View to return json with costs statistic. Has following attribute:

        service -- cost's service

    """

    service = CostService()

    def get(self, request):
        """Return json with cost's statistic for the month"""
        data = self.service.get_statistic_for_the_last_month(
            owner=request.user
        )
        return JsonResponse(data, safe=False)


class StatisticPageView(RenderAuthorizedView):

    """
    Abstract view to return statistic with entries fot the month.
    Has following attributes:

        context_object_name -- entry name in template

    """

    context_object_name = 'object'

    def get(self, request):
        """Render template with entries for the month"""
        entries_for_the_month = self.service.get_for_the_last_month(
            owner=request.user
        )
        total_sum = self.service.get_total_sum(entries_for_the_month)

        context = {
            self.context_object_name: entries_for_the_month,
            'total_sum': total_sum
        }
        return render(request, self.template_name, context)


class CostsStatisticPageView(StatisticPageView):

    """
    View to return statistic with costs for the month.
    Has following attributes:

        service -- cost's service

        template_name -- template to display statistic with costs

        context_object_name -- name of costs in template

    """

    service = CostService()
    template_name = 'costs/costs_statistic.html'
    context_object_name = 'costs'


class IncomesStatisticPageView(StatisticPageView):

    """
    View to return statistic with incomes for the month.
    Has following attributes:

        service -- income's service

        template_name -- template to display statistic with incomes

        context_object_name -- name of incomes in template

    """

    service = IncomeService()
    template_name = 'costs/incomes_statistic.html'
    context_object_name = 'incomes'

