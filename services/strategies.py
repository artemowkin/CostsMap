from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import Model
from djservices.strategies import UserCRUDStrategy


User = get_user_model()


class CreateUniqueCRUDStrategy(UserCRUDStrategy):
    """User CRUD strategy with unique creating"""

    def create(self, form_data: dict, user: User) -> Model:
        """Create a new model entry if entry with the same
        data doesn't exist. Else just return existing entry
        """
        user_kwarg = self._get_user_kwarg(user)
        entry, created = self.model.objects.get_or_create(
            **form_data, **user_kwarg
        )
        return entry
