import datetime
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from generics.unittests import (
    GetEntriesForTheDateTest, GetEntriesServiceTest
)
from costs.services.base import (
    GetCostsForTheDateService, GetCostsService, GetCostsTotalSumService,
    CreateCostService, ChangeCostService, DeleteCostService,
    GetStatisticForTheMonthService, GetStatisticForTheYearService,
    GetAverageCostsForTheDayService
)
from costs.models import Cost
from categories.models import Category


User = get_user_model()


class BaseServiceTest(TestCase):
    """Base class for service tests"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(
            title='test_category', owner=self.user
        )
        self.entry = Cost.objects.create(
            title='test_cost', costs_sum='100.00', owner=self.user,
            category=self.category
        )


class GetCostsForTheDateServiceTest(BaseServiceTest, GetEntriesForTheDateTest):
    """Case of testing GetCostsForTheDateService"""

    def setUp(self):
        super().setUp()
        self.service = GetCostsForTheDateService(self.user)
        self.today = datetime.date.today()


class GetCostsServiceTest(BaseServiceTest, GetEntriesServiceTest):
    """Case of testing GetCostsService"""

    def setUp(self):
        super().setUp()
        self.service = GetCostsService(self.user)


class GetCostsTotalSumServiceTest(BaseServiceTest):
    """Case of testing GetCostsTotalSumService"""

    def setUp(self):
        super().setUp()
        self.service = GetCostsTotalSumService()

    def test_execute(self):
        """Test: does service execute method with costs queryset return
        correct total costs sum
        """
        costs = Cost.objects.all()
        total_sum = self.service.execute(costs)
        self.assertEqual(str(total_sum), self.entry.costs_sum)


class CreateCostServiceTest(BaseServiceTest):
    """Case of testing CreateCostService"""

    def test_execute(self):
        """Test: does service execute method create a new cost"""
        cost_data = {
            'title': 'new_cost', 'costs_sum': '100.00',
            'category': self.category.pk, 'owner': self.user.pk
        }
        cost = CreateCostService.execute(cost_data)
        self.assertTrue(cost.pk)
        self.assertEqual(cost.title, 'new_cost')
        self.assertNotEqual(cost, self.entry)


class ChangeCostServiceTest(BaseServiceTest):
    """Case of testing ChangeCostService"""

    def test_execute(self):
        """Test: does service execute method change the existing cost"""
        cost_data = {
            'cost': self.entry, 'title': 'new_cost', 'costs_sum': '100.00',
            'category': self.category.pk, 'owner': self.user.pk
        }
        cost = ChangeCostService.execute(cost_data)
        all_costs = Cost.objects.all()

        self.assertEqual(cost.pk, self.entry.pk)
        self.assertEqual(cost.title, 'new_cost')
        self.assertEqual(len(all_costs), 1)


class DeleteCostServiceTest(BaseServiceTest):
    """Case of testing DeleteCostService"""

    def test_execute(self):
        """Test: does service execute method delete the existing cost"""
        cost_data = {
            'cost': self.entry, 'owner': self.user.pk
        }
        DeleteCostService.execute(cost_data)
        all_costs = Cost.objects.all()
        self.assertEqual(len(all_costs), 0)


class GetStatisticForTheMonthServiceTest(BaseServiceTest):
    """Case of testing GetStatisticForTheMonthService"""

    def setUp(self):
        super().setUp()
        self.today = datetime.date.today()

    def test_get_statistic_for_the_current_month(self):
        """Test: does execute method return correct statistic for
        the current month
        """
        statistic = GetStatisticForTheMonthService.execute({
            'user': self.user, 'date': self.today
        })
        self.assertEqual(statistic, [{
            'category': self.category.title,
            'costs': Decimal(self.entry.costs_sum)
        }])

    def test_get_statistic_for_the_another_month(self):
        """Test: does execute method not return any statistic for
        the another month
        """
        statistic = GetStatisticForTheMonthService.execute({
            'user': self.user, 'date': datetime.date(2020, 1, 1)
        })
        self.assertEqual(statistic, [])


class GetStatisticForTheYearServiceTest(BaseServiceTest):
    """Case of testing GetStatisticForTheYearService"""

    def setUp(self):
        super().setUp()
        self.today = datetime.date.today()

    def test_get_statistic_for_the_current_year(self):
        """Test: does execute method return correct statistic for
        the current year
        """
        statistic = GetStatisticForTheYearService.execute({
            'user': self.user, 'date': self.today
        })
        self.assertEqual(statistic, [{
            'cost_month': float(self.today.month),
            'cost_sum': Decimal(self.entry.costs_sum)
        }])

    def test_get_statistic_for_the_another_year(self):
        """Test: does execute method not return any statistic for
        the another year
        """
        statistic = GetStatisticForTheYearService.execute({
            'user': self.user, 'date': datetime.date(2020, 1, 1)
        })
        self.assertEqual(statistic, [])


class GetAverageCostsForTheDayServiceTest(BaseServiceTest):
    """Case of testing GetAverageCostsForTheDayService"""

    def test_execute_returns_correct_data(self):
        average_costs = GetAverageCostsForTheDayService.execute({
            'user': self.user
        })
        self.assertEqual(average_costs, Decimal(self.entry.costs_sum))
