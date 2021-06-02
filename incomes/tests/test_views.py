from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class ViewTest(TestCase):
    """Base test class for views"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )


class GetCreateIncomesViewTest(ViewTest):
    """Case of testing GetCreateIncomesView"""
    
    def test_get_with_logged_in_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('all_incomes'))
        self.assertEqual(response.status_code, 200)

    def test_get_with_unlogged_in_user(self):
        response = self.client.get(reverse('all_incomes'))
        self.assertEqual(response.status_code, 403)
