from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from utils.models import ModelWithUUID


User = get_user_model()


class Income(ModelWithUUID):
    """Income model

    Attributes
    ----------
    incomes_sum : DecimalField
        Sum of income
    owner : ForeignKey(User)
        Income owner
    date : DateField
        Income publication date
    pub_datetime : DateTimeField
        Income publication datetime. Needed for ordering

    Methods
    -------
    get_absolute_url()
        Return path to page with incomes with the same date field

    """

    incomes_sum = models.DecimalField(max_digits=7, decimal_places=2)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='incomes'
    )
    date = models.DateField(auto_now_add=True)
    pub_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'income'
        ordering = ('-pub_datetime',)

    def __str__(self):
        return f"Income: {self.incomes_sum}"

    def get_absolute_url(self):
        return reverse('incomes_for_the_date', args=[self.date.isoformat()])
