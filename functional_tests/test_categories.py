import time

from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from django.contrib.auth import get_user_model

from costs.models import Cost
from categories.models import Category
from .base import FunctionalTest


User = get_user_model()


class CategoriesTest(FunctionalTest):
    """Functional tests for categories"""

    def setUp(self):
        super().setUp()
        self.browser.get(self.live_server_url + reverse('category_list'))
        time.sleep(1)

    def test_categories_list(self):
        self.assertEqual(self.browser.title, 'Categories')
        create_button = self.browser.find_element_by_class_name(
            'create_button'
        )
        self.assertEqual(create_button.text, 'Add Category')
        categories_titles = self._get_categories_titles()
        self.assertEqual(categories_titles, [
            'Еда', 'Здоровье', 'Одежда', 'Развлечения', 'Транспорт'
        ])

    def test_create_category(self):
        self.browser.get(self.live_server_url + reverse('create_category'))
        self.assertEqual(self.browser.title, 'Add Category')
        form_title = self.browser.find_element_by_class_name('form_title')
        self.assertEqual(form_title.text, 'Add Category')
        form_input = self.browser.find_element_by_name('title')
        form_input.send_keys('Test Category')
        form_input.send_keys(Keys.ENTER)
        time.sleep(1.5)

        # User redirectes on categories list page
        self.assertEqual(self.browser.title, 'Categories')
        categories_titles = self._get_categories_titles()
        self.assertIn('Test Category', categories_titles)

    def test_category_costs_without_costs(self):
        category = self.browser.find_elements_by_xpath(
            "//*[contains(text(), 'Еда')]"
        )[0]
        category.click()
        self.assertEqual(self.browser.title, 'Еда')
        title = self.browser.find_element_by_class_name('history_header')
        self.assertEqual(title.text, 'Category: "Еда"')
        empty_text = self.browser.find_element_by_class_name('empty_text')
        self.assertEqual(
            empty_text.text, "You don't have any costs in this category"
        )

    def test_category_costs_with_costs(self):
        user = User.objects.get(email="testuser@gmail.com")
        food_category = Category.objects.get(title="Еда")
        cost = Cost.objects.create(
            title="testcost", costs_sum="100.00", category=food_category,
            owner=user
        )
        category = self.browser.find_elements_by_xpath(
            "//*[contains(text(), 'Еда')]"
        )[0]
        category.click()
        self.assertEqual(self.browser.title, 'Еда')
        title = self.browser.find_element_by_class_name('history_header')
        self.assertEqual(title.text, 'Category: "Еда"')
        cost_title = self.browser.find_element_by_class_name('costs_title')
        self.assertEqual(
            cost_title.text, cost.title
        )

    def test_change_category(self):
        self._click_change_category('Еда')
        self.assertEqual(self.browser.title, 'Change Category')
        form_title = self.browser.find_element_by_class_name('form_title')
        self.assertEqual(form_title.text, 'Change Category "Еда"')
        form_title = self.browser.find_element_by_name('title')
        self.assertEqual(form_title.get_attribute('value'), "Еда")
        form_title.send_keys(' (edited)')
        form_title.send_keys(Keys.ENTER)
        time.sleep(2)

        # User redirects on categories list page with edited category
        self.assertEqual(self.browser.title, 'Categories')
        categories_titles = self._get_categories_titles()
        self.assertIn('Еда (edited)', categories_titles)

    def test_delete_category(self):
        self._click_change_category('Еда')
        delete_button = self.browser.find_element_by_class_name('form_delete')
        self.assertEqual(delete_button.text, 'Delete')
        delete_button.click()
        time.sleep(1)
        self.assertEqual(self.browser.title, 'Delete Category')
        form_title = self.browser.find_element_by_class_name('form_title')
        self.assertEqual(form_title.text, 'Delete category "Еда"')
        delete_button = self.browser.find_element_by_class_name('form_delete')
        self.assertEqual(delete_button.text, 'Delete Category')
        delete_button.click()
        time.sleep(1)

        # User redirects on categories list page without Test Category (edited)
        self.assertEqual(self.browser.title, 'Categories')
        categories_titles = self._get_categories_titles()
        self.assertNotIn('Еда', categories_titles)

    def _get_categories_titles(self):
        categories = self.browser.find_elements_by_class_name(
            'category_title'
        )
        categories_titles = [category.text for category in categories]
        return categories_titles

    def _click_change_category(self, title):
        categories = self.browser.find_elements_by_class_name('category')
        new_category = [
            category for category in categories
            if category.find_element_by_class_name(
                'category_title').text == title
        ][0]
        edit_button = new_category.find_element_by_class_name(
            'category_edit_button'
        )
        edit_link = edit_button.get_attribute('href')
        self.browser.get(edit_link)
        time.sleep(1)
