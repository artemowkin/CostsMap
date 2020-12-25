from django import forms
from .models import Income


class IncomeForm(forms.ModelForm):
    """Income form to create/update incomes

    Attributes
    ----------
    incomes_sum : DecimalField
        Sum of income

    """

    class Meta:
        model = Income
        fields = ('incomes_sum',)
