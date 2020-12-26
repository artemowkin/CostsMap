import datetime
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Income
import services.common as services_common


User = get_user_model()


class IncomesServicesTest(TestCase):

    def setUp(self):
        self.today = datetime.date.today()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.instance = Income.objects.create(
            incomes_sum='35.00', owner=self.user
        )

    def test_get_all_user_entries(self):
        all_user_incomes = services_common.get_all_user_entries(
            Income, self.user
        )
        self.assertEqual(len(all_user_incomes), 1)
        self.assertEqual(all_user_incomes[0], self.instance)

    def test_get_total_sum(self):
        incomes = services_common.get_all_user_entries(Income, self.user)
        incomes_sum = services_common.get_total_sum(incomes)
        income = Income.objects.get(pk=self.instance.pk, owner=self.user)
        self.assertEqual(incomes_sum, Decimal(income.incomes_sum))

    def test_get_for_the_month(self):
        incomes = services_common.get_for_the_month(
            Income, self.user, self.today
        )
        self.assertEqual(incomes[0].date.month, self.today.month)

    def test_get_for_the_date(self):
        incomes = services_common.get_for_the_date(
            Income, self.user, self.today
        )
        self.assertEqual(incomes[0].date, self.today)


class IncomesViewsTests(TestCase):

    def setUp(self):
        self.today = datetime.date.today()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.bad_user = User.objects.create_superuser(
            username='baduser', password='badpass'
        )
        self.income = Income.objects.create(
            incomes_sum='100.00', owner=self.user
        )
        self.client.login(username='testuser', password='testpass')

    def test_incomes_for_the_date_view(self):
        response = self.client.get(reverse('today_incomes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/incomes.html')
        self.assertContains(response, self.income.incomes_sum)

    def test_incomes_for_the_date_view_with_dates(self):
        response = self.client.get(
            reverse('incomes_for_the_date', args=[self.today.isoformat()])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/incomes.html')
        self.assertContains(response, self.income.incomes_sum)
        response = self.client.get(
            reverse('incomes_for_the_date', args=['2020-01-01'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/incomes.html')
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
        self.assertTemplateUsed(response, 'incomes/change_income.html')
        response = self.client.post(
            reverse('change_income', args=[self.income.pk]), {
                'incomes_sum': '100'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.client.login(username='baduser', password='badpass')
        bad_response = self.client.get(
            reverse('change_income', args=[self.income.pk])
        )
        self.assertEqual(bad_response.status_code, 404)

    def test_delete_income_view(self):
        response = self.client.get(
            reverse('delete_income', args=[self.income.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/delete_income.html')
        response = self.client.post(
            reverse('delete_income', args=[self.income.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.client.login(username='baduser', password='badpass')
        bad_response = self.client.get(
            reverse('delete_income', args=[self.income.pk])
        )
        self.assertEqual(bad_response.status_code, 404)

    def test_incomes_history_view(self):
        response = self.client.get(reverse('incomes_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/history_incomes.html')
        self.assertContains(response, self.income.incomes_sum)

    def test_incomes_statistic_page_view(self):
        response = self.client.get(
            reverse('incomes_statistic_for_this_month')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/incomes_statistic.html')
        self.assertContains(response, self.income.incomes_sum)

    def test_incomes_statistic_page_view_with_date(self):
        response = self.client.get(
            reverse('incomes_statistic_page', args=['2020-01'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/incomes_statistic.html')
        self.assertNotContains(response, self.income.incomes_sum)
        self.assertNotContains(response, 'canvas')
        self.assertNotContains(response, 'profit')
