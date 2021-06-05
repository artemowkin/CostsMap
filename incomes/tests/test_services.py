import datetime
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from generics.unittests import (
	GetEntriesForTheDateTest, GetEntriesServiceTest
)
from incomes.services.base import (
	GetIncomesForTheDateService, GetIncomesService, GetIncomesTotalSumService,
	CreateIncomeService, ChangeIncomeService, DeleteIncomeService
)
from incomes.models import Income


User = get_user_model()


class BaseServiceTest(TestCase):
	"""Base class for service tests"""

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.entry = Income.objects.create(
			incomes_sum='100.00', owner=self.user
		)


class GetIncomesForTheDateServiceTest(BaseServiceTest, GetEntriesForTheDateTest):
	"""Case of testing GetIncomesForTheDateService"""

	def setUp(self):
		super().setUp()
		self.service = GetIncomesForTheDateService(self.user)
		self.today = datetime.date.today()


class GetIncomesServiceTest(BaseServiceTest, GetEntriesServiceTest):
	"""Case of testing GetIncomesService"""

	def setUp(self):
		super().setUp()
		self.service = GetIncomesService(self.user)


class GetIncomesTotalSumServiceTest(BaseServiceTest):
	"""Case of testing GetIncomesTotalSumService"""

	def setUp(self):
		super().setUp()
		self.service = GetIncomesTotalSumService()

	def test_execute(self):
		"""Test: does service execute method with incomes queryset return
		correct total incomes sum
		"""
		incomes = Income.objects.all()
		total_sum = self.service.execute(incomes)
		self.assertEqual(str(total_sum), self.entry.incomes_sum)


class CreateIncomeServiceTest(BaseServiceTest):
	"""Case of testing CreateIncomeService"""

	def test_execute(self):
		"""Test: does service execute method create a new income"""
		income_data = {'incomes_sum': '100.00', 'owner': self.user.pk}
		income = CreateIncomeService.execute(income_data)
		self.assertTrue(income.pk)
		self.assertEqual(income.incomes_sum, Decimal('100.00'))
		self.assertNotEqual(income, self.entry)


class ChangeIncomeServiceTest(BaseServiceTest):
	"""Case of testing ChangeIncomeService"""

	def test_execute(self):
		"""Test: does service execute method change the existing income"""
		income_data = {
			'income': self.entry, 'incomes_sum': '200.00',
			'owner': self.user.pk
		}
		income = ChangeIncomeService.execute(income_data)
		all_incomes = Income.objects.all()

		self.assertEqual(income.pk, self.entry.pk)
		self.assertEqual(income.incomes_sum, Decimal('200.00'))
		self.assertEqual(len(all_incomes), 1)


class DeleteIncomeServiceTest(BaseServiceTest):
	"""Case of testing DeleteIncomeService"""

	def test_execute(self):
		"""Test: does service execute method delete the existing income"""
		income_data = {'income': self.entry, 'owner': self.user.pk}
		DeleteIncomeService.execute(income_data)
		all_incomes = Income.objects.all()
		self.assertEqual(len(all_incomes), 0)
