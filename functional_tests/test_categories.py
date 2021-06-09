import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from .base import CRUDFunctionalTest
from categories.models import Category


User = get_user_model()


class CategoriesAPIEndpointsTest(TestCase, CRUDFunctionalTest):
	"""Functional test for categories api endpoints"""

	all_endpoint = 'all_categories'
	concrete_endpoint = 'concrete_category'
	model = Category

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.bad_user = User.objects.create_superuser(
			username='baduser', password='badpass'
		)
		self.client.login(username='testuser', password='testpass')
		self.entry = Category.objects.create(
			title='test_category', owner=self.user
		)
		self.serialized_entry = {
			'pk': str(self.entry.pk), 'title': 'test_category',
			'owner': self.user.pk
		}

	def get_all_response(self):
		return [self.serialized_entry]

	def get_all_bad_response(self):
		return []

	def get_create_data(self):
		return {'title': 'some_category'}

	def get_update_data(self):
		return {'title': 'some_category'}
