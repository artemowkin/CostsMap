from django import forms

from categories.models import Category
from .models import Cost


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
