import datetime
import simplejson as json

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
        self.client.login(username='testuser', password='testpass')
        self.income = Income.objects.create(
            incomes_sum='100.00', owner=self.user
        )
        serialized_income = {
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
