import uuid

from django.db import models


class ModelWithUUID(models.Model):
    """Abstract model with UUID primary key field

    Attributes
    ----------
    uuid : UUIDField
        Primary key uuid field

    """

    uuid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4
    )

    class Meta:
        abstract = True
