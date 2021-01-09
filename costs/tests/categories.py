import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..services.categories import CategoryService, DEFAULT_CATEGORIES
from ..models import Cost, Category
from ..forms import CostForm


User = get_user_model()


class CategoryServiceTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.instance = Category.objects.create(
            title='Test category', owner=self.user
        )
        self.cost = Cost.objects.create(
            title='testcost', costs_sum='100.00',
            owner=self.user, category=self.instance
        )
        self.service = CategoryService()

    def test_get_category_costs(self):
        category = self.service.get_concrete(self.instance.pk, self.user)
        costs = self.service.get_category_costs(category)

        self.assertEqual(costs[0], self.cost)
        self.assertEqual(len(costs), 1)

    def test_set_user_default_categories(self):
        self.service.set_user_default_categories(self.user)
        new_categories = self.user.categories.all()

        self.assertEqual(
            len(new_categories), len(DEFAULT_CATEGORIES)+1
        )

    def test_set_form_user_categories(self):
        form = CostForm()
        self.service.set_form_user_categories(form, self.user)
        categories = self.service.get_all(self.user)
        form_queryset = form.fields['category'].queryset

        self.assertEqual(
            len(form_queryset), len(categories)
        )
        for entry in form_queryset:
            self.assertIn(entry, categories)


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
