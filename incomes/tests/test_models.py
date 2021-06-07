import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Income


User = get_user_model()


class IncomeModelTest(TestCase):
	"""Case of testing Income model"""

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.income = Income.objects.create(
			incomes_sum='100.00', owner=self.user
		)

	def test_was_created(self):
		"""Test: was income entry created"""
		self.assertEqual(Income.objects.count(), 1)
		self.assertEqual(Income.objects.first(), self.income)

	def test_created_entry_fields(self):
		"""Test: are created entry's fields correct"""
		self.assertEqual(self.income.incomes_sum, '100.00')
		self.assertEqual(self.income.owner, self.user)

	def test_string_representation(self):
		"""Test: does str(income) returns income title"""
		self.assertEqual(str(self.income), f"Income: {self.income.incomes_sum}")

	def test_pk_is_uuid(self):
		"""Test: is primary key field UUID"""
		self.assertIsInstance(self.income.pk, uuid.UUID)
