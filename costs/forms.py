from django import forms
from django.contrib.auth import get_user_model

from .models import Cost, Category


User = get_user_model()


class CostForm(forms.Form):

    """
    Form for Cost model with following fields:

        title -- cost's title

        costs_sum -- cost's sum

        category -- cost's category

    """

    title = forms.CharField(max_length=255)
    costs_sum = forms.DecimalField(max_digits=7, decimal_places=2)
    category = forms.ModelChoiceField(queryset=Category.objects.all())


class CategoryForm(forms.Form):

    """
    Form for Category model with following fields:

        title -- title of category

    """

    title = forms.CharField(max_length=50)

