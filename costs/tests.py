"""Module with cost's tests"""

import datetime
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Cost, Category, Income
from .services.costs import CostService
from .services.categories import CategoryService
from .services.incomes import IncomeService


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


class DatesTests:

    def test_get_for_the_month(self):
        entries = self.service.get_for_the_month(self.user, self.today)
        self.assertEqual(entries[0].date.month, self.today.month)

    def test_get_for_the_date(self):
        entries = self.service.get_for_the_date(
            self.user, self.today
        )
        self.assertEqual(entries[0].date, self.today)


class CostServiceTest(TestCase, CRUDTests, DatesTests):

    def setUp(self):
        self.service = CostService()
        self.today = datetime.date.today()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(
            title='Test category', owner=self.user
        )
        self.income = Income.objects.create(
            incomes_sum='50.00', owner=self.user
        )
        self.instance = Cost.objects.create(
            title='Test cost', costs_sum='35.00',
            category=self.category, owner=self.user
        )

    def test_get_total_sum(self):
        costs = self.service.get_all(self.user)
        costs_sum = self.service.get_total_sum(costs)
        cost = self.service.get_concrete(self.instance.pk, self.user)
        self.assertEqual(costs_sum, cost.costs_sum)

    def test_get_profit_for_the_month(self):
        profit = self.service.get_profit_for_the_month(self.user, self.today)
        incomes = Decimal(self.income.incomes_sum)
        costs = Decimal(self.instance.costs_sum)
        self.assertEqual(profit, incomes-costs)

    def test_get_statistic_for_the_month(self):
        cost = self.service.get_concrete(self.instance.pk, self.user)
        correct_statistic = [{
            'category': self.category.title,
            'costs': cost.costs_sum
        }]
        statistic = self.service.get_statistic_for_the_month(
            self.user, self.today
        )
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

    def test_get_create_form(self):
        form = self.service.get_create_form(self.user)
        self.assertEqual(form.is_bound, False)

    def test_change_form(self):
        form = self.service.get_change_form(self.instance.pk, self.user)
        self.assertEqual(form.is_bound, True)


class IncomeServiceTest(TestCase, CRUDTests):

    def setUp(self):
        self.service = IncomeService()
        self.today = datetime.date.today()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.instance = Income.objects.create(
            incomes_sum='35.00', owner=self.user
        )

    def test_get_total_sum(self):
        incomes = self.service.get_all(self.user)
        incomes_sum = self.service.get_total_sum(incomes)
        income = self.service.get_concrete(self.instance.pk, self.user)
        self.assertEqual(incomes_sum, income.incomes_sum)

    def test_create(self):
        form_data = {
            'incomes_sum': '40.00',
        }
        instance = self.service.create(form_data, self.user)
        self.assertIsInstance(instance, Income)
        all_instances = self.service.get_all(self.user)
        self.assertEqual(len(all_instances), 2)
        self.assertEqual(instance.incomes_sum, Decimal('40.00'))
        self.assertEqual(instance.owner, self.user)

    def test_change(self):
        form_data = {
            'incomes_sum': '50.00',
        }
        instance = self.service.change(
            form_data, self.instance.pk, self.user
        )
        self.assertIsInstance(instance, Income)
        self.assertEqual(instance.incomes_sum, Decimal('50.00'))
        self.assertEqual(instance.owner, self.user)

    def test_get_create_form(self):
        form = self.service.get_create_form()
        self.assertEqual(form.is_bound, False)

    def test_change_form(self):
        form = self.service.get_change_form(self.instance.pk, self.user)
        self.assertEqual(form.is_bound, True)


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

