import datetime
import uuid
from decimal import Decimal

from django.test import TestCase
from django.http import Http404
from django.contrib.auth import get_user_model

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
		self.income = Income.objects.create(
			incomes_sum='100.00', owner=self.user
		)


class GetIncomesForTheDateServiceTest(BaseServiceTest):
	"""Case of testing GetIncomesForTheDateService"""

	def setUp(self):
		super().setUp()
		self.service = GetIncomesForTheDateService(self.user)
		self.today = datetime.date.today()

	def test_get_for_the_today_month(self):
		"""Test: does get_for_the_month return user incomes for the
		current month
		"""
		incomes = self.service.get_for_the_month(self.today)
		self.assertEqual(len(incomes), 1)
		self.assertEqual(incomes[0], self.income)

	def test_get_for_the_another_month(self):
		"""Test: does get_for_the_month not return any incomes for
		the another month
		"""
		incomes = self.service.get_for_the_month(datetime.date(2020, 1, 1))
		self.assertEqual(len(incomes), 0)

	def test_get_for_the_today(self):
		"""Test: does get_for_the_date return user incomes for the today"""
		incomes = self.service.get_for_the_date(self.today)
		self.assertEqual(len(incomes), 1)
		self.assertEqual(incomes[0], self.income)

	def test_get_for_the_another_day(self):
		"""Test: does get_for_the_date not return any incomes
		for the another day
		"""
		incomes = self.service.get_for_the_date(datetime.date(2020, 1, 1))
		self.assertEqual(len(incomes), 0)


class GetIncomesServiceTest(BaseServiceTest):
	"""Case of testing GetIncomesService"""

	def setUp(self):
		super().setUp()
		self.service = GetIncomesService(self.user)

	def test_get_concrete_with_correct_pk(self):
		"""Test: does get_concrete return a concrete income with
		correct income pk
		"""
		income = self.service.get_concrete(self.income.pk)
		self.assertEqual(income, self.income)

	def test_get_concrete_with_incorrect_pk(self):
		"""Test: does get_concrete not return incomes if pk is incorrect"""
		with self.assertRaises(Http404):
			income = self.service.get_concrete(uuid.uuid4())

	def test_get_all(self):
		"""Test: does get_all method return all user incomes"""
		incomes = self.service.get_all()
		self.assertEqual(len(incomes), 1)
		self.assertEqual(incomes[0], self.income)


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
		self.assertEqual(str(total_sum), self.income.incomes_sum)


class CreateIncomeServiceTest(BaseServiceTest):
	"""Case of testing CreateIncomeService"""

	def test_execute(self):
		"""Test: does service execute method create a new income"""
		income_data = {'incomes_sum': '100.00', 'owner': self.user.pk}
		income = CreateIncomeService.execute(income_data)
		self.assertTrue(income.pk)
		self.assertEqual(income.incomes_sum, Decimal('100.00'))
		self.assertNotEqual(income, self.income)


class ChangeIncomeServiceTest(BaseServiceTest):
	"""Case of testing ChangeIncomeService"""

	def test_execute(self):
		"""Test: does service execute method change the existing income"""
		income_data = {
			'income': self.income, 'incomes_sum': '200.00',
			'owner': self.user.pk
		}
		income = ChangeIncomeService.execute(income_data)
		all_incomes = Income.objects.all()

		self.assertEqual(income.pk, self.income.pk)
		self.assertEqual(income.incomes_sum, Decimal('200.00'))
		self.assertEqual(len(all_incomes), 1)


class DeleteIncomeServiceTest(BaseServiceTest):
	"""Case of testing DeleteIncomeService"""

	def test_execute(self):
		"""Test: does service execute method delete the existing income"""
		income_data = {'income': self.income, 'owner': self.user.pk}
		DeleteIncomeService.execute(income_data)
		all_incomes = Income.objects.all()
		self.assertEqual(len(all_incomes), 0)
