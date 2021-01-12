import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import get_object_or_404

import costs.services.categories as category_services
import services.common as common_services
from ..models import Cost, Category
from ..forms import CostForm


User = get_user_model()


class CategoryServiceTests(TestCase):

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

    def test_get_concrete_user_entry_with_category_model(self):
        category = common_services.get_concrete_user_entry(
            Category, self.category.pk, self.user
        )

        self.assertEqual(category, self.category)

    def test_get_all_user_entries_with_category_model(self):
        all_categories = common_services.get_all_user_entries(
            Category, self.user
        )

        self.assertEqual(len(all_categories), 1)
        self.assertEqual(all_categories[0], self.category)

    def test_create_entry_with_category_model(self):
        category_data = {'title': 'new_category', 'owner': self.user}

        category = common_services.create_entry(Category, category_data)

        self.assertEqual(category.title, category_data['title'])
        self.assertEqual(category.owner, category_data['owner'])

    def test_change_entry_with_category_model(self):
        category_data = {'title': 'new_title'}

        common_services.change_entry(self.category, category_data)

        self.assertEqual(self.category.title, category_data['title'])

    def test_delete_entry_with_category_model(self):
        common_services.delete_entry(self.category)
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
