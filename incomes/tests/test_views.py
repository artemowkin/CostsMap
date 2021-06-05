from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy

from generics.unittests import (
    GetCreateEntriesViewTest, GetUpdateDeleteEntryViewTest,
    GetEntriesForTheMonthViewTest, GetEntriesForTheDateViewTest
)
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


class GetUpdateDeleteIncomeViewTest(ViewTest, GetUpdateDeleteEntryViewTest):
    """Case of testing GetUpdateDeleteIncomeView"""

    endpoint = 'concrete_income'

    def setUp(self):
        super().setUp()
        self.entry = Income.objects.create(
            incomes_sum='100.00', owner=self.user
        )

    def request_put(self):
        return self.client.put(
            reverse('concrete_income', args=[self.entry.pk]), {
                'incomes_sum': '200.00'
            }, content_type='application/json'
        )


class GetIncomesForTheMonthViewTest(ViewTest, GetEntriesForTheMonthViewTest):
    """Case of testing GetIncomesForTheMonthView"""

    endpoint = 'month_incomes'


class GetIncomesForTheDateViewTest(ViewTest, GetEntriesForTheDateViewTest):
    """Case of testing GetIncomesForTheDateView"""

    endpoint = 'date_incomes'
