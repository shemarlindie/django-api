from django.contrib.auth import get_user_model
from django.db import models


class BaseModel(models.Model):
    date_created = models.DateTimeField(
        'date created',
        auto_now_add=True,
        editable=False,
    )
    date_updated = models.DateTimeField(
        'date last updated',
        auto_now=True,
        editable=False,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        models.RESTRICT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created_by",
        editable=False,
    )
    modified_by = models.ForeignKey(
        get_user_model(),
        models.RESTRICT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_modified_by",
        editable=False,
    )

    class Meta:
        abstract = True
