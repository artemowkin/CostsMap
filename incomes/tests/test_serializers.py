from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Income
from ..serializers import IncomeSerializer


User = get_user_model()


class IncomeSerializerTest(TestCase):
	"""Case of testing income serializer"""

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.income = Income.objects.create(
			incomes_sum='100.00', owner=self.user
		)
		self.serializer = IncomeSerializer(self.income)

	def test_has_serializer_all_needed_fields(self):
		self.assertEqual(self.serializer.data['pk'], str(self.income.pk))
		self.assertEqual(self.serializer.data['incomes_sum'], '100.00')
		self.assertEqual(self.serializer.data['owner'], self.user.pk)
		self.assertEqual(
			self.serializer.data['date'], self.income.date.isoformat()
		)
