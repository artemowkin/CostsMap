import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Category


User = get_user_model()


class CategoryModelTest(TestCase):
    """Case of testing category model"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(
                title='test_category', owner=self.user
        )

    def test_was_created(self):
        """Test: was category entry created"""
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.first(), self.category)

    def test_created_entry_fields(self):
        """Test: are created entry's fields correct"""
        self.assertEqual(self.category.title, 'test_category')
        self.assertEqual(self.category.owner, self.user)

    def test_string_representation(self):
        """Test: does str(category) returns category title"""
        self.assertEqual(str(self.category), self.category.title)

    def test_pk_is_uuid(self):
        """Test: is primary key field UUID"""
        self.assertIsInstance(self.category.pk, uuid.UUID)
