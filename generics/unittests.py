import datetime
import uuid

from django.http import Http404


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
