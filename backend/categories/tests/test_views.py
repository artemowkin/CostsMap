from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Category
from costs.models import Cost
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


class GetCategoryCostsViewTest(ViewTest):
    """Case of testing GetCategoryCostsView"""

    def setUp(self):
        super().setUp()
        self.client.login(username='testuser', password='testpass')
        self.category = Category.objects.create(
            title='test_category', owner=self.user
        )
        self.cost = Cost.objects.create(
            title='test_cost', costs_sum='100.00', category=self.category,
            owner=self.user
        )
        self.serialized_cost = {
            'title': 'test_cost', 'costs_sum': 100.0,
            'category': self.category.pk, 'owner': self.user.pk
        }

    def test_get(self):
        response = self.client.get(
            reverse('category_costs', args=[self.category.pk])
        )
        self.assertEqual(response.status_code, 200)
