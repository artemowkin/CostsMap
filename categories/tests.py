"""Module with categories tests"""

import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from utils.tests import CRUDTests, DatesTests

from costs.models import Cost
from .models import Category
from .services import CategoryService


User = get_user_model()


class CategoryServiceTest(TestCase, CRUDTests):

    def setUp(self):
        self.service = CategoryService()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.instance = Category.objects.create(
            title='Test category', owner=self.user
        )

    def test_change(self):
        form_data = {
            'title': 'New title',
            'owner': self.user
        }
        instance = self.service.change(
            form_data, self.instance.pk, self.user
        )
        self.assertIsInstance(instance, Category)
        self.assertEqual(instance.title, 'New title')
        self.assertEqual(instance.owner, self.user)

    def test_create(self):
        form_data = {
            'title': 'New title',
            'owner': self.user
        }
        instance = self.service.create(form_data, self.user)
        self.assertIsInstance(instance, Category)
        all_instances = self.service.get_all(self.user)
        self.assertEqual(len(all_instances), 2)
        self.assertEqual(instance.title, 'New title')
        self.assertEqual(instance.owner, self.user)

    def test_set_default_categories(self):
        self.service.set_default_categories(self.user)
        new_categories = self.user.categories.all()
        self.assertGreater(len(new_categories), 1)

    def test_get_category_costs(self):
        costs = self.service.get_category_costs(self.instance.pk, self.user)
        self.assertEqual(costs.count(), 0)


class CategoriesViewsTests(TestCase):

    def setUp(self):
        self.today = datetime.date.today()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(
            title='testcategory', owner=self.user
        )
        self.cost = Cost.objects.create(
            title='testtitle', costs_sum='100.00',
            category=self.category, owner=self.user
        )
        self.client.login(username='testuser', password='testpass')

    def test_category_list_view(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/category_list.html')
        self.assertContains(response, self.category.title)

    def test_costs_by_category_view(self):
        response = self.client.get(
            reverse('category_costs', args=[self.category.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/costs_by_category.html')
        self.assertContains(response, self.cost.title)
        self.assertContains(response, self.category.title)

    def test_create_category_view(self):
        response = self.client.get(reverse('create_category'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('create_category'), {
            'title': 'some_title',
        })
        self.assertEqual(response.status_code, 302)

    def test_change_category_view(self):
        response = self.client.get(
            reverse('change_category', args=[self.category.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/change_category.html')
        response = self.client.post(
            reverse('change_category', args=[self.category.pk]), {
                'title': 'some_title',
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_category_view(self):
        response = self.client.get(
            reverse('delete_category', args=[self.category.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/delete_category.html')
        response = self.client.post(
            reverse('delete_category', args=[self.category.pk])
        )
        self.assertEqual(response.status_code, 302)

