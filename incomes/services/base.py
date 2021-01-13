from django import forms
from service_objects.services import Service
from django.contrib.auth import get_user_model

from services.common import (
    GetTotalSumService, GetUserEntriesService, GetForTheDateService
)
from ..models import Income


User = get_user_model()


class GetIncomesForTheDateService(GetForTheDateService):
    """Service to get incomes for the date"""

    model = Income


class GetIncomesService(GetUserEntriesService):
    """Service to get user incomes"""

    model = Income


class GetIncomesTotalSumService(GetTotalSumService):
    """Service to get total sum of incomes in queryset"""

    sum_field_name = 'incomes_sum'


class CreateIncomeService(Service):
    """Service to create new incomes"""

    incomes_sum = forms.DecimalField(max_digits=7, decimal_places=2)
    owner = forms.ModelChoiceField(queryset=User.objects.all())
    _model = Income

    def process(self) -> Income:
        """Create a new income"""
        incomes_sum = self.cleaned_data['incomes_sum']
        owner = self.cleaned_data['owner']

        income = self._model.objects.create(
            incomes_sum=incomes_sum, owner=owner
        )
        return income


class ChangeIncomeService(Service):
    """Service to change a concrete income"""

    income = forms.ModelChoiceField(queryset=Income.objects.all())
    incomes_sum = forms.DecimalField(max_digits=7, decimal_places=2)

    def process(self) -> Income:
        """Change a concrete income from `income` attribute"""
        income = self.cleaned_data['income']
        incomes_sum = self.cleaned_data['incomes_sum']

        income.incomes_sum = incomes_sum
        income.save()
        return income


class DeleteIncomeService(Service):
    """Service to delete a concrete income"""

    income = forms.ModelChoiceField(queryset=Income.objects.all())

    def process(self) -> None:
        """Delete a concrete income from `income` attribute"""
        income = self.cleaned_data['income']
        income.delete()
