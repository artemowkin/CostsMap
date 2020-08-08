"""Module with cost's models"""

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from categories.models import Category
from utils.models import ModelWithUUID


User = get_user_model()


class Cost(ModelWithUUID):

    """Cost model

    Fields
    ------
    title : CharField
        Cost's title

    cost_sum : DecimalField
        Sum of cost

    category : ForeignKey(Category)
        Cost's category

    owner : ForeignKey(User)
        Cost's owner

    date : DateField
        Cost's date

    pub_datetime : DateTimeField
        Cost's publication date and time. Needs for ordering


    Meta
    ----
    db_table = 'cost'

    ordering = ('-pub_datetime',)

    Methods
    -------
    get_absolute_url()
        Return page with costs with the same date field

    """

    title = models.CharField(max_length=255)
    costs_sum = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='costs'
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='costs'
    )
    date = models.DateField(auto_now_add=True)
    pub_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cost'
        ordering = ('-pub_datetime',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('costs_for_the_date', args=[self.date.isoformat()])

