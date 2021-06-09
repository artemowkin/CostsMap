import datetime
import simplejson as json
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from .base import CRUDFunctionalTest
from incomes.models import Income


User = get_user_model()


class IncomesAPIEndpointsTest(TestCase, CRUDFunctionalTest):
    """Functional test for incomes api endpoints"""

    all_endpoint = 'all_incomes'
    concrete_endpoint = 'concrete_income'
    month_endpoint = 'month_incomes'
    date_endpoint = 'date_incomes'
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

    def get_month_response(self):
        return {
            'total_sum': float(self.entry.incomes_sum),
            'incomes': [self.serialized_entry]
        }

    def get_another_month_response(self):
        return {'total_sum': 0.0, 'incomes': []}

    def get_today_response(self):
        return {
            'total_sum': float(self.entry.incomes_sum),
            'incomes': [self.serialized_entry]
        }

    def get_another_date_response(self):
        return {'total_sum': 0.0, 'incomes': []}
