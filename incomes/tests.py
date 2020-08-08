"""Module with income's tests"""

import datetime
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from utils.tests import CRUDTests, DatesTests

from .models import Income
from .services import IncomeService


User = get_user_model()


class IncomeServiceTest(TestCase, CRUDTests, DatesTests):

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


class IncomesViewsTests(TestCase):

    def setUp(self):
        self.today = datetime.date.today()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.income = Income.objects.create(
            incomes_sum='100.00', owner=self.user
        )
        self.client.login(username='testuser', password='testpass')

    def test_incomes_for_the_date_view(self):
        response = self.client.get(reverse('today_incomes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/incomes.html')
        self.assertContains(response, self.income.incomes_sum)

    def test_incomes_for_the_date_view_with_dates(self):
        response = self.client.get(
            reverse('incomes_for_the_date', args=[self.today.isoformat()])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/incomes.html')
        self.assertContains(response, self.income.incomes_sum)
        response = self.client.get(
            reverse('incomes_for_the_date', args=['2020-01-01'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/incomes.html')
        self.assertNotContains(response, self.income.incomes_sum)

    def test_create_income_view(self):
        response = self.client.get(reverse('create_income'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('create_income'), {
            'incomes_sum': '100'
        })
        self.assertEqual(response.status_code, 302)

    def test_change_income_view(self):
        response = self.client.get(
            reverse('change_income', args=[self.income.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/change_income.html')
        response = self.client.post(
            reverse('change_income', args=[self.income.pk]), {
                'incomes_sum': '100'
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_income_view(self):
        response = self.client.get(
            reverse('delete_income', args=[self.income.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/delete_income.html')
        response = self.client.post(
            reverse('delete_income', args=[self.income.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_incomes_history_view(self):
        response = self.client.get(reverse('incomes_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/history_incomes.html')
        self.assertContains(response, self.income.incomes_sum)

    def test_incomes_statistic_page_view(self):
        response = self.client.get(
            reverse('incomes_statistic_for_this_month')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/incomes_statistic.html')
        self.assertContains(response, self.income.incomes_sum)

    def test_incomes_statistic_page_view_with_date(self):
        response = self.client.get(
            reverse('incomes_statistic_page', args=['2020-01'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/incomes_statistic.html')
        self.assertNotContains(response, self.income.incomes_sum)
        self.assertNotContains(response, 'canvas')
        self.assertNotContains(response, 'profit')

