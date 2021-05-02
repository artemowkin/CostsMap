from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from categories.models import Category


User = get_user_model()


class ViewTest(TestCase):
    """Base test for views"""

    def setUp(self):
        self.client.login(username="testuser", password="testpass")


class GetCreateCostsViewTest(TestCase):
    """Case of testing GetCreateCostsView"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="testuser", password="testpass"
        )
        self.category = Category.objects.create(
            title="some_category", owner=self.user
        )

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
