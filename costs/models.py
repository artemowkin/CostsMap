"""Module with cost's models"""

import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class ModelWithUUID(models.Model):

    """Abstract model with UUID primary key field"""

    uuid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4
    )

    class Meta:
        abstract = True


class Category(ModelWithUUID):

    """
    Category of cost with following fields:

        title -- category's title

        owner -- category's owner. Foreign key to User model

    """

    title = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='categories'
    )

    class Meta:
        db_table = 'category'
        ordering = ('title',)
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_list')


class Cost(ModelWithUUID):

    """
    Cost with the following fields:

        title -- cost's title

        cost_sum -- decimal sum of cost

        category -- cost's category

        owner -- cost's owner. Foreign key to User model

        date -- cost's date

        pub_datetime -- cost's publication date and time. Needs for ordering

    And following methods:

        get_absolute_url -- return page with costs with the same date field

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

