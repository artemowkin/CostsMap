import datetime
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from incomes.models import Income

import services.common as services_common
from . import services
from .models import Cost, Category
from .forms import CostForm


User = get_user_model()


class CostsServicesTests(TestCase):

    def setUp(self):
        self.today = datetime.date.today()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(
            title='Test category', owner=self.user
        )
        self.income = Income.objects.create(
            incomes_sum='50.00', owner=self.user
        )
        self.instance = Cost.objects.create(
            title='Test cost', costs_sum='35.00',
            category=self.category, owner=self.user
        )

    def test_get_all_user_entries(self):
        all_user_costs = services_common.get_all_user_entries(
            Cost, self.user
        )
        self.assertEqual(len(all_user_costs), 1)
        self.assertEqual(all_user_costs[0], self.instance)

    def test_get_total_sum(self):
        costs = services_common.get_all_user_entries(Cost, self.user)
        costs_sum = services_common.get_total_sum(costs)
        self.assertEqual(costs_sum, Decimal(self.instance.costs_sum))

    def test_get_profit_for_the_month(self):
        profit = services_common.get_profit_for_the_month(
            self.user, self.today
        )
        incomes = Decimal(self.income.incomes_sum)
        costs = Decimal(self.instance.costs_sum)
        self.assertEqual(profit, incomes-costs)

    def test_get_statistic_for_the_month(self):
        correct_statistic = [{
            'category': self.category.title,
            'costs': Decimal(self.instance.costs_sum)
        }]
        statistic = services.get_costs_statistic_for_the_month(
            self.user, self.today
        )
        self.assertEqual(statistic, correct_statistic)

    def test_get_statistic_for_the_year(self):
        correct_statistic = [{
            'cost_month': self.today.month,
            'cost_sum': Decimal(self.instance.costs_sum)
        }]
        statistic = services.get_costs_statistic_for_the_year(
            self.user, self.today
        )
        self.assertEqual(statistic, correct_statistic)

    def test_get_average_costs_for_the_day(self):
        avg = services.get_average_costs_for_the_day(self.user)
        self.assertEqual(avg, Decimal(self.instance.costs_sum))

    def test_get_for_the_month(self):
        costs = services_common.get_for_the_month(
            Cost, self.user, self.today
        )
        self.assertEqual(costs[0].date.month, self.today.month)

    def test_get_for_the_date(self):
        costs = services_common.get_for_the_date(
            Cost, self.user, self.today
        )
        self.assertEqual(costs[0].date, self.today)


class CostsViewsTests(TestCase):

    def setUp(self):
        self.today = datetime.date.today()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(
            title='testcategory', owner=self.user
        )
        self.cost = Cost.objects.create(
            title='testcost', costs_sum='100.00',
            owner=self.user, category=self.category
        )
        self.client.login(username='testuser', password='testpass')

    def test_costs_for_the_date_view(self):
        response = self.client.get(reverse('today_costs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/costs.html')
        self.assertContains(response, self.cost.title)

    def test_costs_for_the_date_view_with_dates(self):
        response = self.client.get(
            reverse('costs_for_the_date', args=[self.today.isoformat()])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/costs.html')
        self.assertContains(response, self.cost.title)
        response = self.client.get(
            reverse('costs_for_the_date', args=['2020-01-01'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/costs.html')
        self.assertNotContains(response, self.cost.title)

    def test_create_cost_view(self):
        response = self.client.get(reverse('create_cost'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/add_cost.html')
        response = self.client.post(reverse('create_cost'), {
            'title': 'some_title',
            'costs_sum': '100',
            'category': self.category.pk
        })
        self.assertEqual(response.status_code, 302)

    def test_change_cost_view(self):
        response = self.client.get(
            reverse('change_cost', args=[self.cost.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/change_cost.html')
        response = self.client.post(
            reverse('change_cost', args=[self.cost.pk]), {
                'title': 'some_title',
                'costs_sum': '100',
                'category': self.category.pk
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_cost_view(self):
        response = self.client.get(
            reverse('delete_cost', args=[self.cost.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/delete_cost.html')
        response = self.client.post(
            reverse('delete_cost', args=[self.cost.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_costs_history_view(self):
        response = self.client.get(reverse('costs_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/history_costs.html')
        self.assertContains(response, self.cost.title)

    def test_statistic_view(self):
        response = self.client.get(
            reverse('statistic', args=[self.today.isoformat()[:-3]])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.title)
        self.assertContains(response, self.cost.costs_sum)

    def test_statistic_for_the_year_view(self):
        response = self.client.get(
            reverse('statistic_for_the_year',
                    args=[self.today.isoformat()[:4]])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, float(self.today.month))
        self.assertContains(response, self.cost.costs_sum)

    def test_costs_statistic_page_view(self):
        response = self.client.get(reverse('costs_statistic_for_this_month'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/costs_statistic.html')
        self.assertContains(response, self.cost.title)
        self.assertContains(response, 'canvas')
        self.assertContains(response, 'profit')

    def test_costs_statistic_page_view_with_date(self):
        response = self.client.get(
            reverse('costs_statistic_page', args=['2020-01'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/costs_statistic.html')
        self.assertNotContains(response, self.cost.title)
        self.assertNotContains(response, 'canvas')
        self.assertNotContains(response, 'profit')


####################
#                  #
#    Categories    #
#                  #
####################


class CategoriesServicesTests(TestCase):

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

    def test_set_default_categories(self):
        services.set_user_default_categories(self.user)
        new_categories = self.user.categories.all()
        self.assertGreater(
            len(new_categories), len(services.DEFAULT_CATEGORIES)
        )

    def test_get_category_costs(self):
        category, costs = services.get_category_costs(
            self.instance.pk, self.user
        )
        self.assertEqual(category, self.instance)
        self.assertEqual(costs[0], self.cost)
        self.assertEqual(costs.count(), 1)

    def test_set_form_owner_categories(self):
        form = CostForm()
        services.set_form_owner_categories(form, self.user)
        categories = services_common.get_all_user_entries(
            Category, self.user
        )
        form_queryset = form.fields['category'].queryset
        self.assertEqual(
            len(form.fields['category'].queryset), len(categories)
        )
        for i in range(len(form_queryset)):
            self.assertEqual(form_queryset[i], categories[i])


class CategoriesViewsTests(TestCase):

    def setUp(self):
        self.today = datetime.date.today()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
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

    def test_create_category_view(self):
        response = self.client.get(reverse('create_category'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('create_category'), {
            'title': 'some_title',
        })
        self.assertEqual(response.status_code, 302)
        bad_response = self.client.post(reverse('create_category'), {
            'title': 'some_title',
        })
        self.assertContains(
            bad_response, 'Category with the same title already exist'
        )

    def test_change_category_view(self):
        response = self.client.get(
            reverse('change_category', args=[self.category.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/change_category.html')
        response = self.client.post(
            reverse('change_category', args=[self.category.pk]), {
                'title': 'some_title',
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_category_view(self):
        response = self.client.get(
            reverse('delete_category', args=[self.category.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'costs/delete_category.html')
        response = self.client.post(
            reverse('delete_category', args=[self.category.pk])
        )
        self.assertEqual(response.status_code, 302)
