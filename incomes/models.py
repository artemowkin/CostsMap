"""Module with income's models"""

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from utils.models import ModelWithUUID


User = get_user_model()


class Income(ModelWithUUID):

    """Income model

    Fields
    ------
    incomes_sum : DecimalField
        sum of income

    owner : ForeignKey(User)
        Income's owner

    date : DateField
        Income's date

    pub_datetime : DateTimeField
        Income's publication date and time. Needs for ordering


    Meta
    ----
    db_table = 'income'

    ordering = ('-pub_datetime',)


    Methods
    -------
    get_absolute_url()
        Return path to incomes page

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
        """Returns path to page with all incomes for income's date"""
        return reverse('incomes_for_the_date', args=[self.date.isoformat()])

