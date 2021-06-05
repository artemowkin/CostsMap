from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy

from generics.unittests import GetCreateEntriesViewTest
from ..models import Income


User = get_user_model()


class ViewTest(TestCase):
    """Base test class for views"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )


class GetCreateIncomesViewTest(ViewTest, GetCreateEntriesViewTest):
    """Case of testing GetCreateIncomesView"""

    endpoint = 'all_incomes'

    def request_post(self):
        return self.client.post(
            reverse('all_incomes'), {
                'title': 'test_income', 'incomes_sum': '100.00'
            }, content_type='application/json'
        )
