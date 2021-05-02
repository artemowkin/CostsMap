import datetime
import simplejson as json
from uuid import UUID

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from categories.models import Category
from costs.models import Cost


User = get_user_model()


class CostsAPIEndpointsTest(TestCase):
    """Functional test for costs api endpoints"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")
        self.category = Category.objects.create(
            title="test_category", owner=self.user
        )
        self.cost = Cost.objects.create(
            title='test_cost', costs_sum='100.00', category=self.category,
            owner=self.user
        )
        self.serialized_cost = {
            'pk': str(self.cost.pk), 'title': 'test_cost',
            'costs_sum': '100.00',
            'category': str(self.category.pk), 'owner': self.user.pk,
            'date': datetime.date.today().isoformat(),
        }

    def test_all_costs_endpoint(self):
        """Test: does /costs/ endpoint return all costs"""
        response = self.client.get('/costs/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, [self.serialized_cost])

    def test_create_cost_endpoint(self):
        response = self.client.post('/costs/', {
            'title': 'some_cost', 'costs_sum': '100.00',
            'category': self.category.pk
        }, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Cost.objects.count(), 2)
        self.assertEqual(Cost.objects.first().title, 'some_cost')

    def test_get_concrete_cost_endpoint(self):
        response = self.client.get(f'/costs/{self.cost.pk}/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, self.serialized_cost)
