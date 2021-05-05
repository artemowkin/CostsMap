from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Cost
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


class GetCreateCostsViewTest(ViewTest):
    """Case of testing GetCreateCostsView"""

    def test_get_with_logged_in_user(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("all_costs"))
        self.assertEqual(response.status_code, 200)

    def test_get_with_unlogged_in_user(self):
        response = self.client.get(reverse("all_costs"))
        self.assertEqual(response.status_code, 403)

    def test_post_with_logged_in_user(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse("all_costs"), {
                'title': 'test_cost', 'costs_sum': '100.00',
                'category': self.category.pk
            }, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_post_with_unlogged_in_user(self):
        response = self.client.post(
            reverse("all_costs"), {
                'title': 'test_cost', 'costs_sum': '100.00',
                'category': self.category.pk
            }, content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)


class GetUpdateDeleteCostViewTest(ViewTest):
    """Case of testing GetUpdateDeleteCostView"""

    def setUp(self):
        super().setUp()
        self.cost = Cost.objects.create(
            title='test_cost', costs_sum='100.00', category=self.category,
            owner=self.user
        )

    def test_get_with_logged_in_user(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(
            reverse('concrete_cost', args=[self.cost.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_get_with_unlogged_in_user(self):
        response = self.client.get(
            reverse('concrete_cost', args=[self.cost.pk])
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_with_logged_in_user(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.delete(
            reverse('concrete_cost', args=[self.cost.pk])
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_with_unlogged_in_user(self):
        response = self.client.delete(
            reverse('concrete_cost', args=[self.cost.pk])
        )
        self.assertEqual(response.status_code, 403)

    def test_put_with_logged_in_user(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.put(
            reverse('concrete_cost', args=[self.cost.pk]), {
                'title': 'some_cost', 'costs_sum': '200.00',
                'category': self.category.pk
            }, content_type="application/json"
        )
        self.assertEqual(response.status_code, 204)

    def test_put_with_unlogged_in_user(self):
        response = self.client.put(
            reverse('concrete_cost', args=[self.cost.pk]), {
                'title': 'some_cost', 'costs_sum': '200.00',
                'category': self.category.pk
            }, content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)


class GetForTheMonthViewTest(ViewTest):
    """Case of testing GetForTheMonthView"""

    def test_get_with_logged_in_user(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(
            reverse("month_costs", args=("2020", "01"))
        )
        self.assertEqual(response.status_code, 200)

    def test_get_with_unlogged_in_user(self):
        response = self.client.get(
            reverse("month_costs", args=("2020", "01"))
        )
        self.assertEqual(response.status_code, 403)


class GetForTheDateViewTest(ViewTest):
    """Case of testing GetForTheDateView"""

    def test_get_with_logged_in_user(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(
            reverse("date_costs", args=("2020", "01", "01"))
        )
        self.assertEqual(response.status_code, 200)

    def test_get_with_unlogged_in_user(self):
        response = self.client.get(
            reverse("date_costs", args=("2020", "01", "01"))
        )
        self.assertEqual(response.status_code, 403)


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
