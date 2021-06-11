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
        Category title
    owner : ForeignKey[User]
        User who created this category

    Methods
    -------
    get_absolute_url()
        Return URL to page with all categories

    """

    title = models.CharField(max_length=50)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='categories'
    )

    class Meta:
        db_table = 'category'
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'owner'), name='unique_for_user',
            ),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('category_list')
