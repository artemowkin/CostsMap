import datetime
import uuid
from decimal import Decimal

from django.test import TestCase
from django.http import Http404
from django.contrib.auth import get_user_model

from generics.unittests import (
    GetEntriesServiceTest
)
from categories.services.base import (
    GetCategoriesService, CreateCategoryService, ChangeCategoryService,
    DeleteCategoryService, SetUserDefaultCategoriesService, get_category_costs
)
from categories.models import Category
from costs.models import Cost


User = get_user_model()


class BaseServiceTest(TestCase):
    """Base class for service tests"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.entry = Category.objects.create(
            title='test_category', owner=self.user
        )


class GetCategoriesServiceTest(BaseServiceTest, GetEntriesServiceTest):
    """Case of testing GetCategories"""

    def setUp(self):
        super().setUp()
        self.service = GetCategoriesService(self.user)


class CreateIncomeServiceTest(BaseServiceTest):
    """Case of testing CreateCategoryService"""

    def test_execute(self):
        """Test: does service execute method create a new category"""
        category_data = {
            'title': 'new_category', 'owner': self.user
        }
        category = CreateCategoryService.execute(category_data)
        self.assertTrue(category.pk)
        self.assertEqual(category.title, 'new_category')
        self.assertNotEqual(category, self.entry)


class ChangeCategoryServiceTest(BaseServiceTest):
    """Case of testing ChangeCategoryService"""

    def test_execute(self):
        """Test: does service execute method change the existing category"""
        category_data = {
            'category': self.entry, 'title': 'new_category',
            'owner': self.user.pk
        }
        category = ChangeCategoryService.execute(category_data)
        all_categories = Category.objects.all()

        self.assertEqual(category.pk, self.entry.pk)
        self.assertEqual(category.title, 'new_category')
        self.assertEqual(len(all_categories), 1)


class DeleteCategoryServiceTest(BaseServiceTest):
    """Case of testing DeleteCategoryService"""

    def test_execute(self):
        """Test: does service execute method delete the existing category"""
        category_data = {'category': self.entry, 'owner': self.user.pk}
        DeleteCategoryService.execute(category_data)
        all_categories = Category.objects.all()
        self.assertEqual(len(all_categories), 0)


class SetUserDefaultCategoriesServiceTest(BaseServiceTest):
    """Case of testing SetUserDefaultCategoriesService"""

    def test_execute(self):
        """Test: does execute method creates the default categories for user"""
        SetUserDefaultCategoriesService.execute({'owner': self.user})
        all_categories = Category.objects.filter(owner=self.user)

        self.assertEqual(all_categories.count(), 6)


class GetCategoryCostsServiceTest(BaseServiceTest):
    """Case of testing get_category_costs service"""

    def test_get_without_costs(self):
        """Test: does get_category_costs return no costs"""
        costs = get_category_costs(self.entry)
        self.assertEqual(costs.count(), 0)

    def test_get_with_costs(self):
        """Test: does get_category_costs return all category costs"""
        cost = Cost.objects.create(
            title='cost_title', costs_sum='100.00', owner=self.user,
            category=self.entry
        )
        costs = get_category_costs(self.entry)
        self.assertEqual(costs.count(), 1)
