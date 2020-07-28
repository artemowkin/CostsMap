import datetime
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Cost, Category
from .services.costs import CostService
from .services.categories import CategoryService


User = get_user_model()


class CRUDTests:

    def test_get_all(self):
        all_instances = self.service.get_all(self.user)
        self.assertEqual(len(all_instances), 1)
        self.assertEqual(all_instances[0], self.instance)

    def test_get_concrete(self):
        instance = self.service.get_concrete(self.instance.pk, self.user)
        self.assertEqual(instance, self.instance)

    def test_delete(self):
        self.service.delete(self.instance.pk, self.user)
        all_instances = self.service.get_all(self.user)
        self.assertEqual(len(all_instances), 0)

    def test_get_create_form(self):
        form = self.service.get_create_form()
        self.assertEqual(form.is_bound, False)

    def test_get_change_form(self):
        form = self.service.get_change_form(self.instance.pk, self.user)
        self.assertEqual(form.is_bound, True)


class CostServiceTest(TestCase, CRUDTests):

    def setUp(self):
        self.service = CostService()
        self.today = datetime.date.today()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(
            title='Test category', owner=self.user
        )
        self.instance = Cost.objects.create(
            title='Test cost', costs_sum='35.00',
            category=self.category, owner=self.user
        )

    def test_get_for_the_last_month(self):
        costs = self.service.get_for_the_last_month(self.user)
        self.assertEqual(costs[0].date.month, self.today.month)

    def test_get_for_the_date(self):
        costs = self.service.get_for_the_date(
            self.user, self.today.isoformat()
        )
        self.assertEqual(costs[0].date, self.today)

    def test_get_sum_of_costs(self):
        costs = self.service.get_all(self.user)
        costs_sum = self.service.get_sum_of_costs(costs)
        self.assertEqual(costs_sum, Decimal('35.00'))

    def test_get_statistic_for_the_last_month(self):
        cost = self.service.get_concrete(self.instance.pk, self.user)
        correct_statistic = [{
            'category': self.category.title,
            'costs': cost.costs_sum
        }]
        statistic = self.service.get_statistic_for_the_last_month(self.user)
        self.assertEqual(statistic, correct_statistic)

    def test_create(self):
        form_data = {
            'title': 'Some title',
            'costs_sum': '40.00',
            'category': self.category
        }
        instance = self.service.create(form_data, self.user)
        self.assertIsInstance(instance, Cost)
        all_instances = self.service.get_all(self.user)
        self.assertEqual(len(all_instances), 2)
        self.assertEqual(instance.title, 'Some title')
        self.assertEqual(instance.costs_sum, Decimal('40.00'))
        self.assertEqual(instance.category, self.category)
        self.assertEqual(instance.owner, self.user)

    def test_change(self):
        form_data = {
            'title': 'New title',
            'costs_sum': '50.00',
            'category': self.category
        }
        instance = self.service.change(
            form_data, self.instance.pk, self.user
        )
        self.assertIsInstance(instance, Cost)
        self.assertEqual(instance.title, 'New title')
        self.assertEqual(instance.costs_sum, Decimal('50.00'))
        self.assertEqual(instance.category, self.category)
        self.assertEqual(instance.owner, self.user)


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

