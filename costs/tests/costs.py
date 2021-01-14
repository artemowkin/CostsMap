import datetime
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from incomes.models import Income
import costs.services as cost_services
from ..services.commands import (
    GetCostsStatisticCommand, GetCostsHistoryCommand,
    GetCostsForTheDateCommand
)
from ..models import Cost, Category
from ..serializers import CostSerializer


User = get_user_model()


class CostServicesTests(TestCase):

    def setUp(self):
        self.today = datetime.date.today()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.bad_user = User.objects.create_user(
            username='testuser2', password='testpass'
        )
        self.category = Category.objects.create(
            title='Test category', owner=self.user
        )
        self.income = Income.objects.create(
            incomes_sum='50.00', owner=self.user
        )
        self.cost = Cost.objects.create(
            title='Test cost', costs_sum='35.00',
            category=self.category, owner=self.user
        )

    def test_create_cost_service(self):
        cost_data = {
            'title': 'new_cost', 'costs_sum': Decimal('100.00'),
            'category': self.category, 'owner': self.user
        }

        cost = cost_services.CreateCostService.execute(cost_data)

        self.assertEqual(cost.title, cost_data['title'])
        self.assertEqual(cost.costs_sum, cost_data['costs_sum'])
        self.assertEqual(cost.category, cost_data['category'])
        self.assertEqual(cost.owner, cost_data['owner'])

    def test_change_cost_service(self):
        change_data = {
            'title': 'new_cost', 'costs_sum': Decimal('100.00'),
            'category': self.category, 'cost': self.cost
        }

        cost = cost_services.ChangeCostService.execute(change_data)

        self.assertEqual(cost.title, change_data['title'])
        self.assertEqual(cost.costs_sum, change_data['costs_sum'])
        self.assertEqual(cost.category, change_data['category'])

    def test_delete_cost_service(self):
        cost_services.DeleteCostService.execute({'cost': self.cost})
        all_costs = Cost.objects.all()

        self.assertEqual(len(all_costs), 0)

    def test_get_statistic_for_the_month(self):
        correct_statistic = [{
            'category': self.category.title,
            'costs': Decimal(self.cost.costs_sum)
        }]
        statistic = cost_services.GetStatisticForTheMonthService.execute({
            'user': self.user,
            'date': self.today
        })

        self.assertEqual(statistic, correct_statistic)

    def test_get_statistic_for_the_year(self):
        correct_statistic = [{
            'cost_month': self.today.month,
            'cost_sum': Decimal(self.cost.costs_sum)
        }]
        statistic = cost_services.GetStatisticForTheYearService.execute({
            'user': self.user,
            'date': self.today
        })

        self.assertEqual(statistic, correct_statistic)

    def test_get_average_costs_for_the_day(self):
        avg = cost_services.GetAverageCostsForTheDayService.execute({
            'user': self.user,
        })

        self.assertEqual(avg, Decimal(self.cost.costs_sum))

    def test_get_total_sum(self):
        costs = cost_services.GetCostsService.get_all(self.user)
        costs_sum = cost_services.GetCostsTotalSumService.execute(costs)

        self.assertEqual(costs_sum, Decimal(self.cost.costs_sum))

    def test_get_for_the_month(self):
        costs = cost_services.GetCostsForTheDateService.get_for_the_month(
            self.user, self.today
        )
        self.assertEqual(costs[0].date.month, self.today.month)

    def test_get_for_the_date(self):
        costs = cost_services.GetCostsForTheDateService.get_for_the_date(
            self.user, self.today
        )
        self.assertEqual(costs[0].date, self.today)

    def test_get_costs_statistic_command(self):
        command = GetCostsStatisticCommand(
            self.user, self.today
        )
        statistic = command.execute()

        costs = cost_services.GetCostsForTheDateService.get_for_the_month(
            self.user, self.today
        )
        costs_sum = cost_services.GetCostsTotalSumService.execute(costs)
        incomes_sum = Decimal(self.income.incomes_sum)
        profit = incomes_sum - costs_sum
        serializer = CostSerializer(costs, many=True)
        right_statistic = {
            'costs': serializer.data,
            'date': self.today,
            'total_sum': costs_sum,
            'profit': profit,
            'average_costs': Decimal(self.cost.costs_sum)
        }

        self.assertEqual(
            len(statistic['costs']), len(right_statistic['costs'])
        )
        self.assertEqual(statistic['costs'][0], right_statistic['costs'][0])
        self.assertEqual(statistic['date'], right_statistic['date'])
        self.assertEqual(statistic['total_sum'], right_statistic['total_sum'])
        self.assertEqual(statistic['profit'], right_statistic['profit'])
        self.assertEqual(
            statistic['average_costs'], right_statistic['average_costs']
        )

    def test_get_costs_history_command(self):
        right_data = {
            'costs': Cost.objects.all(),
            'total_sum': Decimal(self.cost.costs_sum)
        }

        command = GetCostsHistoryCommand(self.user)
        data = command.execute()
        serialized_cost = CostSerializer(self.cost).data

        self.assertEqual(len(right_data['costs']), len(data['costs']))
        self.assertEqual(serialized_cost, data['costs'][0])
        self.assertEqual(right_data['total_sum'], data['total_sum'])

    def test_get_costs_for_the_date_command(self):
        right_data = {
            'costs': Cost.objects.all(),
            'total_sum': Decimal(self.cost.costs_sum),
            'date': self.today
        }

        command = GetCostsForTheDateCommand(self.user, self.today)
        data = command.execute()
        serialized_cost = CostSerializer(self.cost).data

        self.assertEqual(len(right_data['costs']), len(data['costs']))
        self.assertEqual(serialized_cost, data['costs'][0])
        self.assertEqual(right_data['total_sum'], data['total_sum'])


class CostsViewsTests(TestCase):

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
        self.cost = Cost.objects.create(
            title='testcost', costs_sum='100.00',
            owner=self.user, category=self.category
        )
        self.client.login(username='testuser', password='testpass')

    def test_costs_for_the_date_view(self):
        response = self.client.get(reverse('today_costs'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.cost.title)

    def test_costs_for_the_date_view_with_right_date(self):
        response = self.client.get(
            reverse('costs_for_the_date', args=[self.today.isoformat()])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.cost.title)

    def test_costs_for_the_date_view_with_bad_date(self):
        response = self.client.get(
            reverse('costs_for_the_date', args=['2020-01-01'])
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.cost.title)

    def test_create_cost_view(self):
        response = self.client.post(reverse('create_cost'), {
            'title': 'some_title',
            'costs_sum': '100',
            'category': self.category.pk
        })
        all_costs = cost_services.GetCostsService.get_all(self.user)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(all_costs), 2)
        self.assertEqual(all_costs[0].title, 'some_title')

    def test_change_cost_view(self):
        response = self.client.post(
            reverse('change_cost', args=[self.cost.pk]), {
                'title': 'some_title',
                'costs_sum': '100',
                'category': self.category.pk
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_change_cost_view_bad_user(self):
        self.client.login(username='baduser', password='badpass')
        bad_response = self.client.post(
            reverse('change_cost', args=[self.cost.pk])
        )

        self.assertEqual(bad_response.status_code, 404)

    def test_delete_cost_view(self):
        response = self.client.post(
            reverse('delete_cost', args=[self.cost.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_cost_view_bad_user(self):
        self.client.login(username='baduser', password='badpass')
        bad_response = self.client.post(
            reverse('delete_cost', args=[self.cost.pk])
        )
        self.assertEqual(bad_response.status_code, 404)

    def test_costs_history_view(self):
        response = self.client.get(reverse('costs_history'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.cost.title)

    def test_costs_statistic_for_the_month_view(self):
        response = self.client.get(
            reverse('statistic_for_the_month',
            args=[self.today.isoformat()[:-3]])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.title)
        self.assertContains(response, float(self.cost.costs_sum))

    def test_costs_statistic_for_the_year_view(self):
        response = self.client.get(
            reverse('statistic_for_the_year',
                    args=[self.today.isoformat()[:4]])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, float(self.today.month))
        self.assertContains(response, float(self.cost.costs_sum))

    def test_costs_statistic_page_view(self):
        response = self.client.get(reverse('costs_statistic_for_this_month'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.cost.title)

    def test_costs_statistic_page_view_with_date(self):
        response = self.client.get(
            reverse('costs_statistic_page', args=['2020-01'])
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.cost.title)
