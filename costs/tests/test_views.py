from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Cost
from generics.unittests import (
    GetCreateEntriesViewTest, GetUpdateDeleteEntryViewTest,
    GetEntriesForTheMonthViewTest, GetEntriesForTheDateViewTest
)
from categories.models import Category


User = get_user_model()


class ViewTest(TestCase):
    """Base test class for views"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="testuser", password="testpass"
        )
        self.category = Category.objects.create(
            title="some_category", owner=self.user
        )


class GetCreateCostsViewTest(ViewTest, GetCreateEntriesViewTest):
    """Case of testing GetCreateCostsView"""

    endpoint = 'all_costs'

    def request_post(self):
        return self.client.post(
            reverse("all_costs"), {
                'title': 'test_cost', 'costs_sum': '100.00',
                'category': self.category.pk
            }, content_type="application/json"
        )


class GetUpdateDeleteCostViewTest(ViewTest, GetUpdateDeleteEntryViewTest):
    """Case of testing GetUpdateDeleteCostView"""

    endpoint = 'concrete_cost'

    def setUp(self):
        super().setUp()
        self.entry = Cost.objects.create(
            title='test_cost', costs_sum='100.00', category=self.category,
            owner=self.user
        )

    def request_put(self):
        return self.client.put(
            reverse('concrete_cost', args=[self.entry.pk]), {
                'title': 'some_cost', 'costs_sum': '200.00',
                'category': self.category.pk
            }, content_type="application/json"
        )


class GetCostsForTheMonthViewTest(ViewTest, GetEntriesForTheMonthViewTest):
    """Case of testing GetCostsForTheMonthView"""

    endpoint = 'month_costs'


class GetCostsForTheDateViewTest(ViewTest, GetEntriesForTheDateViewTest):
    """Case of testing GetCostsForTheDateView"""

    endpoint = 'date_costs'


class CostsMonthStatisticView(ViewTest):
    """Case of testing CostsMonthStatisticView"""

    def test_get_with_logged_in_user(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(
            reverse("costs_statistic_month", args=("2020", "01"))
        )
        self.assertEqual(response.status_code, 200)

    def test_get_with_unlogged_in_user(self):
        response = self.client.get(
            reverse("costs_statistic_month", args=("2020", "01"))
        )
        self.assertEqual(response.status_code, 403)


class CostsYearStatisticView(ViewTest):
    """Case of testing CostsYearStatisticView"""

    def test_get_with_logged_in_user(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(
            reverse("costs_statistic_year", args=("2020",))
        )
        self.assertEqual(response.status_code, 200)

    def test_get_with_unlogged_in_user(self):
        response = self.client.get(
            reverse("costs_statistic_year", args=("2020",))
        )
        self.assertEqual(response.status_code, 403)


class AverageCostsView(ViewTest):
    """Case of testing AverageCostsView"""

    def test_get_with_logged_in_user(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get('/costs/statistic/average/')
        self.assertEqual(response.status_code, 200)

    def test_get_with_unlogged_in_user(self):
        response = self.client.get('/costs/statistic/average/')
        self.assertEqual(response.status_code, 403)
