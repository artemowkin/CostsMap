from django.test import TestCase
from django.contrib.auth import get_user_model

from categories.models import Category
from ..models import Cost
from ..serializers import CostSerializer


User = get_user_model()


class CostSerializerTest(TestCase):
    """Case of testing cost seiralizer"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="testuser", password="testpass"
        )
        self.category = Category.objects.create(
            title="test_category", owner=self.user
        )
        self.cost = Cost.objects.create(
            title="test_cost", costs_sum="100.00", category=self.category,
            owner=self.user
        )
        self.serializer = CostSerializer(self.cost)

    def test_has_serializer_all_needed_fields(self):
        self.assertEqual(self.serializer.data['pk'], str(self.cost.pk))
        self.assertEqual(self.serializer.data['title'], 'test_cost')
        self.assertEqual(self.serializer.data['costs_sum'], '100.00')
        self.assertEqual(self.serializer.data['category'], self.category.pk)
        self.assertEqual(self.serializer.data['owner'], self.user.pk)
        self.assertEqual(
            self.serializer.data['date'], self.cost.date.isoformat()
        )
