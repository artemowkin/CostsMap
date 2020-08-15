"""Module with cost's tests"""

import datetime
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from utils.tests import CRUDTests, DatesTests
from incomes.models import Income
from categories.models import Category

from .models import Cost
from .services import CostService


User = get_user_model()


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

    def test_get_statistic_for_the_last_year(self):
        cost = self.service.get_concrete(self.instance.pk, self.user)
        correct_statistic = [{
            'cost_month': self.today.month,
            'cost_sum': cost.costs_sum
        }]
        statistic = self.service.get_statistic_for_the_last_year(self.user)
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


class CostsViewsTests(TestCase):

    def setUp(self):
        self.today = datetime.date.today()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(
            title='testcategory', owner=self.user
        )
        self.cost = Cost.objects.create(
            title='testcost', costs_sum='100.00',
            owner=self.user, category=self.category
        )
        self.client.login(username='testuser', password='testpass')

    def test_costs_for_the_date_view(self):
        response = self.client.get(reverse('today_costs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/costs.html')
        self.assertContains(response, self.cost.title)

    def test_costs_for_the_date_view_with_dates(self):
        response = self.client.get(
            reverse('costs_for_the_date', args=[self.today.isoformat()])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/costs.html')
        self.assertContains(response, self.cost.title)
        response = self.client.get(
            reverse('costs_for_the_date', args=['2020-01-01'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/costs.html')
        self.assertNotContains(response, self.cost.title)

    def test_create_cost_view(self):
        response = self.client.get(reverse('create_cost'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/add_cost.html')
        response = self.client.post(reverse('create_cost'), {
            'title': 'some_title',
            'costs_sum': '100',
            'category': self.category.pk
        })
        self.assertEqual(response.status_code, 302)

    def test_change_cost_view(self):
        response = self.client.get(
            reverse('change_cost', args=[self.cost.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/change_cost.html')
        response = self.client.post(
            reverse('change_cost', args=[self.cost.pk]), {
                'title': 'some_title',
                'costs_sum': '100',
                'category': self.category.pk
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_cost_view(self):
        response = self.client.get(
            reverse('delete_cost', args=[self.cost.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/delete_cost.html')
        response = self.client.post(
            reverse('delete_cost', args=[self.cost.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_costs_history_view(self):
        response = self.client.get(reverse('costs_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/history_costs.html')
        self.assertContains(response, self.cost.title)

    def test_statistic_view(self):
        response = self.client.get(
            reverse('statistic', args=[self.today.isoformat()[:-3]])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.title)
        self.assertContains(response, self.cost.costs_sum)

    def test_costs_statistic_page_view(self):
        response = self.client.get(reverse('costs_statistic_for_this_month'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/costs_statistic.html')
        self.assertContains(response, self.cost.title)
        self.assertContains(response, 'canvas')
        self.assertContains(response, 'profit')

    def test_costs_statistic_page_view_with_date(self):
        response = self.client.get(
            reverse('costs_statistic_page', args=['2020-01'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/costs_statistic.html')
        self.assertNotContains(response, self.cost.title)
        self.assertNotContains(response, 'canvas')
        self.assertNotContains(response, 'profit')

