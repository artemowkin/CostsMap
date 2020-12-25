from django import forms

from .models import Category, Cost


class CategoryForm(forms.ModelForm):
    """Category form to create/update categories"""

    class Meta:
        model = Category
        fields = ('title', )


class CostForm(forms.ModelForm):
    """Cost form to create/update costs

    Attributes
    ----------
    category : ModelChoiceField
        Category choice field without default label

    """

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label=None
    )

    class Meta:
        model = Cost
        fields = ('title', 'costs_sum', 'category')
