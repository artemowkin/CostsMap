"""Module with cost's forms"""

from django import forms
from django.contrib.auth import get_user_model

from categories.models import Category


User = get_user_model()


class CostForm(forms.Form):

    """Form for Cost model

    Fields
    ------
    title : CharField
        Cost's title

    costs_sum : DecimalField
        Cost's sum

    category : ModelChoiceField
        Cost's category

    """

    title = forms.CharField(max_length=255)
    costs_sum = forms.DecimalField(max_digits=7, decimal_places=2)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label=None
    )

