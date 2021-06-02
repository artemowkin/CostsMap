import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet

from .base import (
	GetIncomesService, GetIncomesTotalSumService, GetIncomesForTheDateService
)
from ..serializers import IncomeSerializer


User = get_user_model()


class ListIncomesCommand:
	"""Base command to get list of incomes"""

	get_service = None
	total_sum_service = GetIncomesTotalSumService()
	serializer_class =  IncomeSerializer

	def __init__(self, user: User):
		if not self.get_service:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have `get_service` attribute"
			)

		self._user = user
		self._service = self.get_service(user)

	def execute(self) -> dict:
		incomes = self.get_incomes()
		total_incomes_sum = self.total_sum_service.execute(incomes)
		serialized_incomes = self.serializer_class(incomes, many=True).data
		return {
			'total_sum': total_incomes_sum, 'incomes': serialized_incomes
		}

	def get_incomes(self):
		"""Abstract method to get list of incomes"""
		pass


class GetAllIncomesCommand(ListIncomesCommand):
	"""Command to get all user incomes"""

	get_service = GetIncomesService

	def get_incomes(self) -> QuerySet:
		return self._service.get_all()


class DateIncomesListCommand(ListCostsCommand):
	"""Base command for commands to get incomes for the date"""

	get_service = GetIncomesForTheDateService

	def __init__(self, user: User, date: datetime.date):
		super().__init__(user)
		self._date = date


class GetIncomesForTheMonthCommand(DateIncomesListCommand):
	"""Command to get user incomes for the concrete month"""

	def get_incomes(self) -> QuerySet:
		return self._service.get_for_the_month(self._date)


class GetIncomesForTheDateCommand(DateIncomesListCommand):
	"""Command to get user incomes for the concrete date"""

	def get_incomes(self) -> QuerySet:
		return self._service.get_for_the_date(self._date)
