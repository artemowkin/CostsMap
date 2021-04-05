import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Category


User = get_user_model()


class CategoriesViewsTests(TestCase):

    def setUp(self):
        self.today = datetime.date.today()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.bad_user = User.objects.create_superuser(
            username='baduser', password='badpass'
        )
        self.category = Category.objects.create(
            title='testcategory', owner=self.user
        )
        self.client.login(username='testuser', password='testpass')

    def test_category_list_view(self):
        """Test: does category list request returns correct response"""
        response = self.client.get(reverse('category_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/category_list.html')

    def test_costs_by_category_view(self):
        """Test: does category costs request returns correct response"""
        response = self.client.get(
            reverse('category_costs', args=[self.category.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/costs_by_category.html')

    def test_create_category_view_get(self):
        """Test: does GET request on create category page
        returns correct response
        """
        response = self.client.get(reverse('create_category'))
        self.assertEqual(response.status_code, 200)

    def test_create_category_view_post(self):
        """Test: does POST request on create category page
        returns correct response
        """
        response = self.client.post(reverse('create_category'), {
            'title': 'some_title',
        })

        self.assertEqual(response.status_code, 302)

    def test_change_category_view_get(self):
        """Test: does GET request on change category page
        returns correct response
        """
        response = self.client.get(
            reverse('change_category', args=[self.category.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/change_category.html')

    def test_change_category_view_post(self):
        """Test: does POST request on change category page
        returns correct response
        """
        response = self.client.post(
            reverse('change_category', args=[self.category.pk]), {
                'title': 'some_title',
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_change_category_view_bad_user(self):
        """Test: does GET request on change category page with
        user who isn't an owner of category returns 404 response
        """
        self.client.login(username='baduser', password='badpass')
        bad_response = self.client.get(
            reverse('change_category', args=[self.category.pk])
        )

        self.assertEqual(bad_response.status_code, 404)

    def test_delete_category_view_get(self):
        """Test: does GET request on delete category page returns
        correct response
        """
        response = self.client.get(
            reverse('delete_category', args=[self.category.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/delete_category.html')

    def test_delete_category_view_post(self):
        """Test: does POST request on delete category page returns
        correct response
        """
        response = self.client.post(
            reverse('delete_category', args=[self.category.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_category_view_bad_user(self):
        """Test: does GET request on delete category page with
        user who isn't an owner of category returns 404 response
        """
        self.client.login(username='baduser', password='badpass')
        bad_response = self.client.get(
            reverse('delete_category', args=[self.category.pk])
        )
        self.assertEqual(bad_response.status_code, 404)
