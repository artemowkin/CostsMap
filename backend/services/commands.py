import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet


User = get_user_model()


class ListEntriesCommand:
    """Base command to get entries list"""

    get_service = None
    total_sum_service = None
    serializer_class = None
    queryset_name = 'objects'

    def __init__(self, user: User):
        if not self.get_service:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `get_service` attribute"
            )
        if not self.total_sum_service:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`total_sum_service` attribute"
            )
        if not self.serializer_class:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`serializer_class` attribute"
            )

        self._user = user
        self._service = self.get_service(user)

    def execute(self) -> dict:
        entries = self.get_entries()
        total_entries_sum = self.total_sum_service.execute(entries)
        serialized_entries = self.serializer_class(entries, many=True).data
        return {
            'total_sum': total_entries_sum,
            self.queryset_name: serialized_entries
        }

    def get_entries(self) -> QuerySet:
        """Get all entries list"""
        return self._service.get_all()


class DateEntriesListCommand(ListEntriesCommand):
    """Base command for commands to get entries for the date"""

    def __init__(self, user: User, date: datetime.date):
        super().__init__(user)
        self._date = date
