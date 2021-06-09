import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from utils.models import ModelWithUUID
from categories.models import Category


User = get_user_model()


class Cost(ModelWithUUID):
    """Cost model

    Attributes
    ----------
    title : CharField
        Cost title
    costs_sum : DecimalField
        Sum of cost
    category : ForeignKey(Category)
        Cost category
    owner : ForeignKey(User)
        Cost owner
    date : DateField
        Cost publication date
    pub_datetime : DateTimeField
        Cost publication datetime. Needed for ordering

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
    date = models.DateField(default=datetime.date.today)
    pub_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cost'
        verbose_name = 'cost'
        verbose_name_plural = 'costs'
        ordering = ('-date', '-pub_datetime')

    def __str__(self):
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('costs_for_the_date', args=[self.date.isoformat()])
