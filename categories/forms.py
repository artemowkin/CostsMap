from django import forms

from .models import Category


class CategoryForm(forms.ModelForm):
    """Category form to create/update categories"""

    class Meta:
        model = Category
        fields = ('title', )
