import datetime
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

import categories.services.categories as category_services
from .services.commands import GetCategoryCostsCommand
from .models import Category
from costs.models import Cost
from costs.forms import CostForm


User = get_user_model()


class CategoryServicesTests(TestCase):

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
        category = category_services.GetCategoriesService.get_concrete(
            self.category.pk, self.user
        )

        self.assertEqual(category, self.category)

    def test_get_categories_service_get_all(self):
        all_categories = category_services.GetCategoriesService.get_all(
            self.user
        )

        self.assertEqual(len(all_categories), 1)
        self.assertEqual(all_categories[0], self.category)

    def test_create_category_service(self):
        category_data = {'title': 'new_category', 'owner': self.user}

        category = category_services.CreateCategoryService.execute(
            category_data
        )

        self.assertEqual(category.title, category_data['title'])
        self.assertEqual(category.owner, category_data['owner'])

    def test_change_category_service(self):
        category_data = {'title': 'new_title', 'category': self.category}

        category = category_services.ChangeCategoryService.execute(
            category_data
        )

        self.assertEqual(category.title, category_data['title'])

    def test_delete_category_service(self):
        category_services.DeleteCategoryService.execute({
            'category': self.category
        })
        all_categories = Category.objects.all()

        self.assertEqual(len(all_categories), 0)

    def test_get_category_costs(self):
        costs = category_services.get_category_costs(self.category)

        self.assertEqual(costs[0], self.cost)
        self.assertEqual(len(costs), 1)

    def test_set_user_default_categories(self):
        category_services.SetUserDefaultCategoriesService.execute({
            'owner': self.user
        })
        new_categories = self.user.categories.all()

        self.assertGreater(len(new_categories), 1)

    def test_set_form_categories(self):
        form = CostForm()
        all_user_categories = Category.objects.filter(owner=self.user)
        category_services.set_form_categories(form, all_user_categories)
        form_queryset = form.fields['category'].queryset

        self.assertEqual(
            len(form_queryset), len(all_user_categories)
        )
        for entry in form_queryset:
            self.assertIn(entry, all_user_categories)

    def test_get_category_costs_command(self):
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


class CategoriesViewsTests(TestCase):

    def setUp(self):
        self.today = datetime.date.today()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.bad_user = User.objects.create_superuser(
            username='baduser', password='badpass'
        )
        self.category = Category.objects.create(
            title='testcategory', owner=self.user
        )
        self.cost = Cost.objects.create(
            title='testtitle', costs_sum='100.00',
            category=self.category, owner=self.user
        )
        self.client.login(username='testuser', password='testpass')

    def test_category_list_view(self):
        response = self.client.get(reverse('category_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/category_list.html')
        self.assertContains(response, self.category.title)

    def test_costs_by_category_view(self):
        response = self.client.get(
            reverse('category_costs', args=[self.category.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/costs_by_category.html')
        self.assertContains(response, self.cost.title)
        self.assertContains(response, self.category.title)

    def test_create_category_view_get(self):
        response = self.client.get(reverse('create_category'))
        self.assertEqual(response.status_code, 200)

    def test_create_category_view_post(self):
        response = self.client.post(reverse('create_category'), {
            'title': 'some_title',
        })

        self.assertEqual(response.status_code, 302)

    def test_change_category_view_get(self):
        response = self.client.get(
            reverse('change_category', args=[self.category.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/change_category.html')

    def test_change_category_view_post(self):
        response = self.client.post(
            reverse('change_category', args=[self.category.pk]), {
                'title': 'some_title',
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_change_category_view_bad_user(self):
        self.client.login(username='baduser', password='badpass')
        bad_response = self.client.get(
            reverse('change_category', args=[self.category.pk])
        )

        self.assertEqual(bad_response.status_code, 404)

    def test_delete_category_view_get(self):
        response = self.client.get(
            reverse('delete_category', args=[self.category.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/delete_category.html')

    def test_delete_category_view_post(self):
        response = self.client.post(
            reverse('delete_category', args=[self.category.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_category_view_bad_user(self):
        self.client.login(username='baduser', password='badpass')
        bad_response = self.client.get(
            reverse('delete_category', args=[self.category.pk])
        )
        self.assertEqual(bad_response.status_code, 404)
