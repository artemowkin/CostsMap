"""Module with models utilities"""

import uuid

from django.db import models


class ModelWithUUID(models.Model):

    """Abstract model with UUID primary key field

    Fields
    ------
    uuid : UUIDField
        Primary key uuid field

    Meta
    ----
    abstract = True

    """

    uuid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4
    )

    class Meta:
        abstract = True

