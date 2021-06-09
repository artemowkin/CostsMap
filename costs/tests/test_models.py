import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model

from categories.models import Category
from ..models import Cost


User = get_user_model()


class CostModelTest(TestCase):
	"""Case of testing cost model"""

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(
			title='test_category', owner=self.user
		)
		self.cost = Cost.objects.create(
			title='test_cost', costs_sum='100.00', category=self.category,
			owner=self.user
		)

	def test_was_created(self):
		"""Test: was cost entry created"""
		self.assertEqual(Cost.objects.count(), 1)
		self.assertEqual(Cost.objects.first(), self.cost)

	def test_created_entry_fields(self):
		"""Test: are created entry's fields correct"""
		self.assertEqual(self.cost.title, 'test_cost')
		self.assertEqual(self.cost.costs_sum, '100.00')
		self.assertEqual(self.cost.category, self.category)
		self.assertEqual(self.cost.owner, self.user)

	def test_string_representation(self):
		"""Test: does str(cost) returns cost title"""
		self.assertEqual(str(self.cost), self.cost.title)

	def test_pk_is_uuid(self):
		"""Test: is primary key field UUID"""
		self.assertIsInstance(self.cost.pk, uuid.UUID)
