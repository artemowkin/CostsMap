"""Module with incomes forms"""

from django import forms
from .models import Income


class IncomeForm(forms.Form):

    """Form for Income model

    Fields
    ------
    incomes_sum : DecimalField
        Income's sum

    """

    incomes_sum = forms.DecimalField(max_digits=7, decimal_places=2)

