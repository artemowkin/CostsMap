import datetime
import simplejson as json
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from incomes.models import Income


User = get_user_model()


class IncomesAPIEndpointsTest(TestCase):
    """Functional test for incomes api endpoints"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.bad_user = User.objects.create_superuser(
            username='baduser', password='badpass'
        )
        self.client.login(username='testuser', password='testpass')
        self.income = Income.objects.create(
            incomes_sum='100.00', owner=self.user
        )
        self.serialized_income = {
            'pk': str(self.income.pk), 'incomes_sum': '100.00',
            'owner': self.user.pk, 'date': datetime.date.today().isoformat()
        }

    def test_all_incomes_endpoint(self):
        """Test: does /incomes/ endpoint return all incomes"""
        response = self.client.get('/incomes/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {
            'total_sum': float(self.income.incomes_sum),
            'incomes': [self.serialized_income]
        })

    def test_all_incomes_endpoint_with_bad_user(self):
        """Test: does /incomes/ endpoint requested by bad user returns no
        user incomes"""
        self.client.login(username='baduser', password='badpass')
        response = self.client.get('/incomes/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {
            'total_sum': 0.0,
            'incomes': []
        })

    def test_create_income_endpoint(self):
        response = self.client.post('/incomes/', {
            'incomes_sum': '500.00'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Income.objects.count(), 2)
        self.assertEqual(Income.objects.first().incomes_sum, Decimal('500.00'))

    def test_get_concrete_income_endpoint(self):
        response = self.client.get(f"/incomes/{self.income.pk}/")
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, self.serialized_income)

    def test_get_concrete_income_endpoint_with_bad_user(self):
        """Test: does get concrete income endpoint requested by bad user
        returns no content"""
        self.client.login(username='baduser', password='badpass')
        response = self.client.get(f"/incomes/{self.income.pk}/")
        self.assertEqual(response.status_code, 404)

    def test_delete_concrete_income_endpoint(self):
        response = self.client.delete(f"/incomes/{self.income.pk}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Income.objects.count(), 0)

    def test_delete_concrete_income_endpoint_with_bad_user(self):
        """Test: does delete a concrete income endpoint requested
        by bad user do nothing"""
        self.client.login(username='baduser', password='badpass')
        response = self.client.delete(f"/incomes/{self.income.pk}/")
        self.assertEqual(response.status_code, 404)

    def test_update_concrete_income_endpoint(self):
        response = self.client.put(
            f"/incomes/{self.income.pk}/", {
                'incomes_sum': '1000.00'
            }, content_type='application/json'
        )
        self.assertEqual(response.status_code, 204)
        income = Income.objects.get(pk=self.income.pk)
        self.assertEqual(income.incomes_sum, Decimal('1000.00'))

    def test_update_concrete_income_endpoint_with_bad_user(self):
        """Test: does update a concrete income endpoint requested
        by bad user do nothing"""
        self.client.login(username='baduser', password='badpass')
        response = self.client.put(
            f"/incomes/{self.income.pk}/", {
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
            'total_sum': float(self.income.incomes_sum),
            'incomes': [self.serialized_income]
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
            'total_sum': float(self.income.incomes_sum),
            'incomes': [self.serialized_income]
        })

    def test_get_incomes_for_the_another_date(self):
        random_date = datetime.date(2020, 1, 1)
        response = self.client.get(
            f"/incomes/{random_date.year}/{random_date.month}/{random_date.day}/"
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, {'total_sum': 0.0, 'incomes': []})
