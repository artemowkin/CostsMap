import datetime
import simplejson as json
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from generics.functional_tests import CRUDFunctionalTest
from incomes.models import Income


User = get_user_model()


class IncomesAPIEndpointsTest(TestCase, CRUDFunctionalTest):
    """Functional test for incomes api endpoints"""

    all_endpoint = 'all_incomes'
    concrete_endpoint = 'concrete_income'
    model = Income

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.bad_user = User.objects.create_superuser(
            username='baduser', password='badpass'
        )
        self.client.login(username='testuser', password='testpass')
        self.entry = Income.objects.create(
            incomes_sum='100.00', owner=self.user
        )
        self.serialized_entry = {
            'pk': str(self.entry.pk), 'incomes_sum': '100.00',
            'owner': self.user.pk, 'date': datetime.date.today().isoformat()
        }

    def get_all_response(self):
        """Test: does /incomes/ endpoint return all incomes"""
        return {
            'total_sum': float(self.entry.incomes_sum),
            'incomes': [self.serialized_entry]
        }

    def get_all_bad_response(self):
        return {
            'total_sum': 0.0,
            'incomes': []
        }

    def get_create_data(self):
        return {
            'incomes_sum': '500.00'
        }

    def get_update_data(self):
        return {
            'incomes_sum': '1000.00'
        }

    def test_update_concrete_income_endpoint_with_bad_user(self):
        """Test: does update a concrete income endpoint requested
        by bad user do nothing"""
        self.client.login(username='baduser', password='badpass')
        response = self.client.put(
            f"/incomes/{self.entry.pk}/", {
                'incomes_sum': '1000.00'
            }, content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_get_incomes_for_the_month(self):
        today = datetime.date.today()
        response = self.client.get(f"/incomes/{today.year}/{today.month}/")
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {
            'total_sum': float(self.entry.incomes_sum),
            'incomes': [self.serialized_entry]
        })

    def test_get_incomes_for_the_another_month(self):
        random_date = datetime.date(2020, 1, 1)
        response = self.client.get(
            f"/incomes/{random_date.year}/{random_date.month}/"
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {'total_sum': 0.0, 'incomes': []})

    def test_get_incomes_for_the_today(self):
        today = datetime.date.today()
        response = self.client.get(
            f"/incomes/{today.year}/{today.month}/{today.day}/"
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {
            'total_sum': float(self.entry.incomes_sum),
            'incomes': [self.serialized_entry]
        })

    def test_get_incomes_for_the_another_date(self):
        random_date = datetime.date(2020, 1, 1)
        response = self.client.get(
            f"/incomes/{random_date.year}/{random_date.month}/{random_date.day}/"
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {'total_sum': 0.0, 'incomes': []})
