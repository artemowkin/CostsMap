"""Module with category's forms"""

from django import forms
from django.contrib.auth import get_user_model

from .models import Category


class CategoryForm(forms.Form):

    """Form for Category model

    Fields
    ------
    title : CharField
        Title of category

    """

    title = forms.CharField(max_length=50)

