import datetime
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Income
import incomes.services as income_services
from .services.commands import (
    GetIncomesStatisticCommand, GetIncomesForTheDateCommand,
    GetIncomesHistoryCommand
)
from utils.date import MonthContextDate, ContextDate
import costs.services as cost_services
from costs.models import Cost, Category


User = get_user_model()


class IncomeServiceTests(TestCase):

    def setUp(self):
        self.today = datetime.date.today()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.income = Income.objects.create(
            incomes_sum='35.00', owner=self.user
        )

    def test_get_incomes_service_get_all(self):
        get_service = income_services.GetIncomesService(self.user)
        all_incomes = get_service.get_all()

        self.assertEqual(len(all_incomes), 1)
        self.assertEqual(all_incomes[0], self.income)

    def test_get_incomes_service_get_concrete(self):
        get_service = income_services.GetIncomesService(self.user)
        income = get_service.get_concrete(self.income.pk)

        self.assertEqual(income, self.income)

    def test_get_incomes_total_sum_service(self):
        get_service = income_services.GetIncomesService(self.user)
        incomes = get_service.get_all()
        incomes_sum = income_services.GetIncomesTotalSumService.execute(
            incomes
        )

        self.assertEqual(incomes_sum, Decimal(self.income.incomes_sum))

    def test_get_incomes_for_the_date_service_get_for_the_month(self):
        income_date_service = income_services.GetIncomesForTheDateService(
            self.user
        )
        incomes = income_date_service.get_for_the_month(self.today)

        self.assertEqual(incomes[0].date.month, self.today.month)

    def test_get_incomes_for_the_date_service_get_for_the_date(self):
        income_date_service = income_services.GetIncomesForTheDateService(
            self.user
        )
        incomes = income_date_service.get_for_the_date(self.today)

        self.assertEqual(incomes[0].date, self.today)

    def test_create_income_service(self):
        income_data = {'incomes_sum': Decimal('100.00'), 'owner': self.user}

        income = income_services.CreateIncomeService.execute(income_data)

        self.assertEqual(income.incomes_sum, income_data['incomes_sum'])
        self.assertEqual(income.owner, income_data['owner'])

    def test_change_income_service(self):
        change_data = {
            'incomes_sum': Decimal('100.00'), 'income': self.income
        }

        income = income_services.ChangeIncomeService.execute(change_data)

        self.assertEqual(income.incomes_sum, change_data['incomes_sum'])

    def test_delete_cost_service(self):
        income_services.DeleteIncomeService.execute({'income': self.income})
        all_incomes = Income.objects.all()

        self.assertEqual(len(all_incomes), 0)

    def test_get_incomes_statistic_command(self):
        command = GetIncomesStatisticCommand(self.user, self.today)
        statistic = command.execute()
        income_date_service = income_services.GetIncomesForTheDateService(
            self.user
        )
        cost_date_service = cost_services.GetCostsForTheDateService(
            self.user
        )
        month_incomes = income_date_service.get_for_the_month(self.today)
        month_costs = cost_date_service.get_for_the_month(self.today)
        incomes_sum = income_services.GetIncomesTotalSumService.execute(
            month_incomes
        )
        right_statistic = {
            'incomes': month_incomes,
            'costs': month_costs,
            'date': MonthContextDate(self.today),
            'total_sum': incomes_sum,
            'profit': incomes_sum,
            'average_costs': Decimal('0.00'),
        }

    def test_get_incomes_history_command(self):
        right_data = {
            'incomes': Income.objects.all(),
            'total_sum': Decimal(self.income.incomes_sum)
        }

        command = GetIncomesHistoryCommand(self.user)
        data = command.execute()

        self.assertEqual(len(right_data['incomes']), len(data['incomes']))
        self.assertEqual(right_data['incomes'][0], data['incomes'][0])
        self.assertEqual(right_data['total_sum'], data['total_sum'])

    def test_get_costs_for_the_date_command(self):
        right_data = {
            'incomes': Income.objects.all(),
            'total_sum': Decimal(self.income.incomes_sum),
            'date': ContextDate(self.today)
        }

        command = GetIncomesForTheDateCommand(self.user, self.today)
        data = command.execute()

        self.assertEqual(len(right_data['incomes']), len(data['incomes']))
        self.assertEqual(right_data['incomes'][0], data['incomes'][0])
        self.assertEqual(right_data['total_sum'], data['total_sum'])


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

    def test_incomes_statistic_page_view_with_cost(self):
        category = Category.objects.create(
            title='test category', owner=self.user
        )
        cost = Cost.objects.create(
            title='Test cost', costs_sum='35.00',
            category=category, owner=self.user
        )
        response = self.client.get(
            reverse('incomes_statistic_for_this_month')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/incomes_statistic.html')
        self.assertContains(response, self.income.incomes_sum)
        self.assertContains(
            response,
            Decimal(self.income.incomes_sum) - Decimal(cost.costs_sum)
        )
        self.assertContains(response, 'canvas')
        self.assertContains(response, 'profit')

    def test_incomes_statistic_page_view_with_date(self):
        response = self.client.get(
            reverse('incomes_statistic_page', args=['2020-01'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/incomes_statistic.html')
        self.assertNotContains(response, self.income.incomes_sum)
        self.assertNotContains(response, 'canvas')
        self.assertNotContains(response, 'profit')
