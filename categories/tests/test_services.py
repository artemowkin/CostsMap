from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..services import categories as category_services
from ..services.commands import GetCategoryCostsCommand
from ..models import Category
from costs.models import Cost
from costs.forms import CostForm


User = get_user_model()


class CategoryServicesTests(TestCase):
    """Case of testing categories services"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(
            title='Test category', owner=self.user
        )
        self.cost = Cost.objects.create(
            title='testcost', costs_sum='100.00',
            owner=self.user, category=self.category
        )

    def test_get_categories_service_get_concrete(self):
        """Test: does GetCategoriesService.get_concrete return
        a correct category
        """
        get_service = category_services.GetCategoriesService(self.user)
        category = get_service.get_concrete(self.category.pk)

        self.assertEqual(category, self.category)

    def test_get_categories_service_get_all(self):
        """Test: does GetCategoriesService.get_all return
        all user categories
        """
        get_service = category_services.GetCategoriesService(self.user)
        all_categories = get_service.get_all()

        self.assertEqual(len(all_categories), 1)
        self.assertEqual(all_categories[0], self.category)

    def test_create_category_service(self):
        """Test: does CreateCategoryService correctly create
        a new category
        """
        category_data = {'title': 'new_category', 'owner': self.user}

        category = category_services.CreateCategoryService.execute(
            category_data
        )

        self.assertEqual(category.title, category_data['title'])
        self.assertEqual(category.owner, category_data['owner'])

    def test_change_category_service(self):
        """Test: does ChangeCategoryService correctly change category"""
        category_data = {'title': 'new_title', 'category': self.category}

        category = category_services.ChangeCategoryService.execute(
            category_data
        )

        self.assertEqual(category.title, category_data['title'])

    def test_delete_category_service(self):
        """Test: does DeleteCategoryService delete a concrete category"""
        category_services.DeleteCategoryService.execute({
            'category': self.category
        })
        all_categories = Category.objects.all()

        self.assertEqual(len(all_categories), 0)

    def test_get_category_costs(self):
        """Test: does get_category_costs return costs in category"""
        costs = category_services.get_category_costs(self.category)

        self.assertEqual(costs[0], self.cost)
        self.assertEqual(len(costs), 1)

    def test_set_user_default_categories(self):
        """Test: does SetUserDefaultCategoriesService correctly set
        default categories for user
        """
        category_services.SetUserDefaultCategoriesService.execute({
            'owner': self.user
        })
        new_categories = self.user.categories.all()

        self.assertGreater(len(new_categories), 1)

    def test_set_form_categories(self):
        """Test: does set_form_categories set correctly user
        categories for form
        """
        form = CostForm()
        all_user_categories = Category.objects.filter(owner=self.user)
        category_services.set_form_categories(form, all_user_categories)
        form_queryset = form.fields['category'].queryset

        self.assertEqual(
            len(form_queryset), len(all_user_categories)
        )
        for entry in form_queryset:
            self.assertIn(entry, all_user_categories)


class CategoryCommandsTest(TestCase):
    """Case of testing categories commands"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(
            title='Test category', owner=self.user
        )
        self.cost = Cost.objects.create(
            title='testcost', costs_sum='100.00',
            owner=self.user, category=self.category
        )

    def test_get_category_costs_command(self):
        """Test: does GetCategoryCostsCommand return category costs"""
        right_context = {
            'category': self.category, 'costs': self.category.costs.all(),
            'total_sum': Decimal(self.cost.costs_sum)
        }

        command = GetCategoryCostsCommand(self.category.pk, self.user)
        context = command.execute()

        self.assertEqual(context['category'], right_context['category'])
        self.assertEqual(len(context['costs']), len(right_context['costs']))
        self.assertEqual(context['costs'][0], right_context['costs'][0])
        self.assertEqual(context['total_sum'], right_context['total_sum'])
