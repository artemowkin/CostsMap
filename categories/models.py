"""Module with categories models"""

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from utils.models import ModelWithUUID


User = get_user_model()


class Category(ModelWithUUID):

    """Category of cost

    Attributes
    ----------
    title : CharField
        Category's title

    owner : ForeignKey(User)
        Category's owner


    Meta
    ----
    db_table = 'category'

    ordering = ('title',)

    verbose_name = 'categories'


    Methods
    -------
    get_absolute_url()
        Return path to costs page

    """

    title = models.CharField(max_length=50)
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

