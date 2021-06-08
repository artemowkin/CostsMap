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
        self.bad_user = User.objects.create_superuser(
            username='baduser', password='badpass'
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
        self.assertEqual(json_response, {
            'total_sum': float(self.cost.costs_sum),
            'costs': [self.serialized_cost]
        })

    def test_all_costs_endpoint_with_bad_user(self):
        """Test: does /costs/ endpoint requested by bad user returns no
        user costs"""
        self.client.login(username='baduser', password='badpass')
        response = self.client.get('/costs/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {
            'total_sum': 0.0,
            'costs': []
        })

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

    def test_get_concrete_cost_endpoint_with_bad_user(self):
        """Test: does get concrete cost endpoint requested by bad user
        returns no content"""
        self.client.login(username='baduser', password='badpass')
        response = self.client.get(f'/costs/{self.cost.pk}/')
        self.assertEqual(response.status_code, 404)

    def test_delete_concrete_cost_endpoint(self):
        response = self.client.delete(f'/costs/{self.cost.pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Cost.objects.count(), 0)

    def test_delete_concrete_cost_endpoint_with_bad_user(self):
        """Test: does delete a concrete cost endpoint requested by bad user
        do nothing"""
        self.client.login(username='baduser', password='badpass')
        response = self.client.delete(f'/costs/{self.cost.pk}/')
        self.assertEqual(response.status_code, 404)

    def test_update_concrete_cost_endpoint(self):
        response = self.client.put(
            f'/costs/{self.cost.pk}/', {
                'title': 'some_cost', 'costs_sum': '200.00',
                'category': self.category.pk
            }, content_type="application/json"
        )
        self.assertEqual(response.status_code, 204)
        cost = Cost.objects.get(pk=self.cost.pk)
        self.assertEqual(str(cost.costs_sum), '200.00')

    def test_update_concrete_cost_endpoint_with_bad_user(self):
        """Test: does update a concrete cost endpoint requested by bad user
        do nothing"""
        self.client.login(username='baduser', password='badpass')
        response = self.client.put(
            f'/costs/{self.cost.pk}/', {
                'title': 'some_cost', 'costs_sum': '200.00',
                'category': self.category.pk
            }, content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_get_costs_for_the_month(self):
        today = datetime.date.today()
        response = self.client.get(f"/costs/{today.year}/{today.month}/")
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {
            'total_sum': float(self.cost.costs_sum),
            'costs': [self.serialized_cost]
        })

    def test_get_costs_for_the_another_month(self):
        random_date = datetime.date(2020, 1, 1)
        response = self.client.get(
            f'/costs/{random_date.year}/{random_date.month}/'
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {'total_sum': 0.0, 'costs': []})

    def test_get_costs_for_the_month_with_bad_user(self):
        today = datetime.date.today()
        response = self.client.get(f"/costs/{today.year}/{today.montb}/")
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {
            'total_sum': 0.0,
            'costs': []
        })

    def test_get_costs_for_the_today(self):
        today = datetime.date.today()
        response = self.client.get(
            f'/costs/{today.year}/{today.month}/{today.day}/'
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {
            'total_sum': float(self.cost.costs_sum),
            'costs': [self.serialized_cost]
        })

    def test_get_costs_for_the_another_date(self):
        random_date = datetime.date(2020, 1, 1)
        response = self.client.get(
            f'/costs/{random_date.year}/{random_date.month}/{random_date.day}/'
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {'total_sum': 0.0, 'costs': []})

    def test_get_costs_for_the_today_with_bad_user(self):
        today = datetime.date.today()
        response = self.client.get(
            f"/costs/{today.year}/{today.month}/{today.day}/"
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {
            'total_sum': 0.0,
            'costs': []
        })

    def test_get_costs_statistic_for_the_month(self):
        today = datetime.date.today()
        response = self.client.get(
            f'/costs/statistic/{today.year}/{today.month}/'
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, [{
            'category': self.category.title,
            'costs': float(self.cost.costs_sum)
        }])

    def test_get_costs_statistic_for_the_year(self):
        today = datetime.date.today()
        response = self.client.get(
            f'/costs/statistic/{today.year}/'
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, [{
            'cost_month': float(self.cost.date.month),
            'cost_sum': float(self.cost.costs_sum)
        }])

    def test_get_average_costs_statistic(self):
        response = self.client.get('/costs/statistic/average/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {
            'average_costs': float(self.cost.costs_sum)
        })
