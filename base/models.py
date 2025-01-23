import uuid

from django.db import models


class UUIDModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    changed_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
