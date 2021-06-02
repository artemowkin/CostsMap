import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet

from services.commands import ListEntriesCommand, DateEntriesListCommand
from .base import (
	GetIncomesService, GetIncomesTotalSumService, GetIncomesForTheDateService
)
from ..serializers import IncomeSerializer


User = get_user_model()


class IncomesListMixin:
	"""Mixin with incomes class attributes"""

	total_sum_service = GetIncomesTotalSumService()
	serializer_class = IncomeSerializer
	queryset_name = 'incomes'


class GetAllIncomesCommand(IncomesListMixin, ListEntriesCommand):
	"""Command to get all user incomes"""

	get_service = GetIncomesService


class GetIncomesForTheMonthCommand(IncomesListMixin, DateEntriesListCommand):
	"""Command to get user incomes for the concrete month"""

	get_service = GetIncomesForTheDateService

	def get_entries(self) -> QuerySet:
		return self._service.get_for_the_month(self._date)


class GetIncomesForTheDateCommand(IncomesListMixin, DateEntriesListCommand):
	"""Command to get user incomes for the concrete date"""

	get_service = GetIncomesForTheDateService

	def get_entries(self) -> QuerySet:
		return self._service.get_for_the_date(self._date)
