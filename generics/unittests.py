import datetime
import uuid

from django.http import Http404
from django.urls import reverse


class GetEntriesForTheDateTest:
	"""Tests for Get<model>ForTheDateService service"""

	def test_get_for_the_today_month(self):
		"""Test: does get_for_the_month return user entries for the
		current month"""
		entries = self.service.get_for_the_month(self.today)
		self.assertEqual(len(entries), 1)
		self.assertEqual(entries[0], self.entry)

	def test_get_for_the_another_month(self):
		"""Test: :does get_for_the_month not return any entries for
		the another month"""
		entries = self.service.get_for_the_month(datetime.date(2020, 1, 1))
		self.assertEqual(len(entries), 0)

	def test_get_for_the_today(self):
		"""Test: does get_for_the_date return user entries for the today"""
		entries = self.service.get_for_the_date(self.today)
		self.assertEqual(len(entries), 1)

	def test_get_for_the_another_day(self):
		"""Test: does get_for_the_date not return any entries
		for the another day"""
		entries = self.service.get_for_the_date(datetime.date(2020, 1, 1))
		self.assertEqual(len(entries), 0)


class GetEntriesServiceTest:
	"""Tests for Get<model>Service service"""

	def test_get_concrete_with_correct_pk(self):
		"""Test: does get_concrete return a concrete entry with
		correct entry pk
		"""
		entry = self.service.get_concrete(self.entry.pk)
		self.assertEqual(entry, self.entry)

	def test_get_concrete_with_incorrect_pk(self):
		"""Test: does get_concrete not return entry if pk is incorrect"""
		with self.assertRaises(Http404):
			entry = self.service.get_concrete(uuid.uuid4())

	def test_get_all(self):
		"""Test: does get_all method return all user entries"""
		entries = self.service.get_all()
		self.assertEqual(len(entries), 1)
		self.assertEqual(entries[0], self.entry)


class GetCreateEntriesViewTest:
	"""Tests for GetCreate<model>View view"""

	def test_get_with_logged_in_user(self):
		self.client.login(username='testuser', password='testpass')
		response = self.client.get(reverse(self.endpoint))
		self.assertEqual(response.status_code, 200)

	def test_get_with_unlogged_in_user(self):
		response = self.client.get(reverse(self.endpoint))
		self.assertEqual(response.status_code, 403)

	def test_post_with_logged_in_user(self):
		self.client.login(username='testuser', password='testpass')
		response = self.request_post()
		self.assertEqual(response.status_code, 201)

	def test_post_with_unlogged_in_user(self):
		response = self.request_post()
		self.assertEqual(response.status_code, 403)

	def request_post(self):
		raise NotImplementedError


class GetUpdateDeleteEntryViewTest:
	"""Case of testing GetUpdateDelete<entry>View view"""

	def test_get_with_logged_in_user(self):
	    self.client.login(username="testuser", password="testpass")
	    response = self.client.get(
	        reverse(self.endpoint, args=[self.entry.pk])
	    )
	    self.assertEqual(response.status_code, 200)

	def test_get_with_unlogged_in_user(self):
	    response = self.client.get(
	        reverse(self.endpoint, args=[self.entry.pk])
	    )
	    self.assertEqual(response.status_code, 403)

	def test_delete_with_logged_in_user(self):
	    self.client.login(username="testuser", password="testpass")
	    response = self.client.delete(
	        reverse(self.endpoint, args=[self.entry.pk])
	    )
	    self.assertEqual(response.status_code, 204)

	def test_delete_with_unlogged_in_user(self):
	    response = self.client.delete(
	        reverse(self.endpoint, args=[self.entry.pk])
	    )
	    self.assertEqual(response.status_code, 403)

	def test_put_with_logged_in_user(self):
	    self.client.login(username="testuser", password="testpass")
	    response = self.request_put()
	    self.assertEqual(response.status_code, 204)

	def test_put_with_unlogged_in_user(self):
	    response = self.request_put()
	    self.assertEqual(response.status_code, 403)
