from django.db import models
from apps.models import (
    CreatedBaseModel,
    CreateUpdatedBaseModel
)
from django.contrib.postgres.fields import JSONField
from apps.properties.models import Property


class Activity(CreateUpdatedBaseModel):
    property = models.ForeignKey(
        Property,
        related_name="property_id",
        on_delete=models.CASCADE,
    )
    schedule = models.DateTimeField()
    title = models.CharField(max_length=255)

    CANCELED = 'c'
    ACTIVE = 'a'
    COMPLETED = 'd'
    STATUS_CHOICES = [
        (CANCELED, 'canceled'),
        (ACTIVE, 'active'),
        (COMPLETED, 'done'),
    ]
    status = models.CharField(
        max_length=35,
        choices=STATUS_CHOICES,
        default=ACTIVE
    )

    class Meta:
        unique_together = ['property', 'schedule']


class Survey(CreatedBaseModel):
    activity = models.OneToOneField(
        Activity,
        on_delete=models.CASCADE,
    )
    answers = JSONField()
