from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Category
from generics.unittests import (
    GetCreateEntriesViewTest, GetUpdateDeleteEntryViewTest
)


User = get_user_model()


class ViewTest(TestCase):
    """Base test class for views"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )


class GetCreateCategoryViewTest(ViewTest, GetCreateEntriesViewTest):
    """Case of testing GetCreateCategoryView"""

    endpoint = 'all_categories'

    def request_post(self):
        return self.client.post(
            reverse('all_categories'), {
                'title': 'new_category'
            }, content_type='application/json'
        )


class GetUpdateDeleteCategoryViewTest(ViewTest, GetUpdateDeleteEntryViewTest):
    """Case of testing GetUpdateDeleteCategoryView"""

    endpoint = 'concrete_category'

    def setUp(self):
        super().setUp()
        self.entry = Category.objects.create(
            title='test_category', owner=self.user
        )

    def request_put(self):
        return self.client.put(
            reverse('concrete_category', args=[self.entry.pk]), {
                'title': 'changed_category'
            }, content_type='application/json'
        )
