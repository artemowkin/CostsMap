import datetime
import simplejson as json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .base import DateCRUDFunctionalTest
from categories.models import Category
from costs.models import Cost


User = get_user_model()


class CostsAPIEndpointsTest(TestCase, DateCRUDFunctionalTest):
    """Functional test for costs api endpoints"""

    all_endpoint = 'all_costs'
    concrete_endpoint = 'concrete_cost'
    month_endpoint = 'month_costs'
    date_endpoint = 'date_costs'
    model = Cost

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="testuser", password="testpass"
        )
        self.bad_user = User.objects.create_superuser(
            username='baduser', password='badpass'
        )
        self.client.login(username="testuser", password="testpass")
        self.category = Category.objects.create(
            title="test_category", owner=self.user
        )
        self.entry = Cost.objects.create(
            title='test_cost', costs_sum='100.00', category=self.category,
            owner=self.user
        )
        self.serialized_entry = {
            'pk': str(self.entry.pk), 'title': 'test_cost',
            'costs_sum': '100.00',
            'category': str(self.category.pk), 'owner': self.user.pk,
            'date': datetime.date.today().isoformat(),
        }

    def get_all_response(self):
        return {
            'total_sum': float(self.entry.costs_sum),
            'costs': [self.serialized_entry]
        }

    def get_all_bad_response(self):
        return {
            'total_sum': 0.0,
            'costs': []
        }

    def get_create_data(self):
        return {
            'title': 'some_cost', 'costs_sum': '100.00',
            'category': self.category.pk
        }

    def test_create_endpoint_with_date(self):
        response = self.client.post(
            reverse(self.all_endpoint), {
                'title': 'some_cost', 'costs_sum': '100.00',
                'category': self.category.pk, 'date': '2020-01-01'
            }, content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.model.objects.count(), 2)
        created_cost = self.model.objects.last()
        self.assertEqual(created_cost.date.isoformat(), '2020-01-01')

    def get_update_data(self):
        return {
            'title': 'some_cost', 'costs_sum': '200.00',
            'category': self.category.pk
        }

    def test_update_endpoint_with_date(self):
        response = self.client.put(
            reverse(self.concrete_endpoint, args=[self.entry.pk]), {
                'title': 'some_cost', 'costs_sum': '200.00',
                'category': self.category.pk, 'date': '2020-01-01'
            }, content_type='application/json'
        )
        self.assertEqual(response.status_code, 204)
        entry = self.model.objects.get(pk=self.entry.pk)
        self.assertNotEqual(str(self.entry), str(entry))
        self.assertEqual(entry.date.isoformat(), '2020-01-01')

    def get_month_response(self):
        return {
            'total_sum': float(self.entry.costs_sum),
            'costs': [self.serialized_entry]
        }

    def get_another_month_response(self):
        return {'total_sum': 0.0, 'costs': []}

    def get_today_response(self):
        return {
            'total_sum': float(self.entry.costs_sum),
            'costs': [self.serialized_entry]
        }

    def get_another_date_response(self):
        return {'total_sum': 0.0, 'costs': []}

    def test_get_costs_statistic_for_the_month(self):
        today = datetime.date.today()
        response = self.client.get(
            f'/costs/statistic/{today.year}/{today.month}/'
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, [{
            'category': self.category.title,
            'costs': float(self.entry.costs_sum)
        }])

    def test_get_costs_statistic_for_the_year(self):
        today = datetime.date.today()
        response = self.client.get(
            f'/costs/statistic/{today.year}/'
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, [{
            'cost_month': float(self.entry.date.month),
            'cost_sum': float(self.entry.costs_sum)
        }])

    def test_get_average_costs_statistic(self):
        response = self.client.get('/costs/statistic/average/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {
            'average_costs': float(self.entry.costs_sum)
        })
