from django.db import models
from apps.models import CreateUpdatedBaseModel


class Property(CreateUpdatedBaseModel):
    title = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    disabled_at = models.DateTimeField(blank=True, null=True)

    ENABLED = 'e'
    DISABLED = 'd'
    STATUS_CHOICES = [
        (ENABLED, 'active'),
        (DISABLED, 'inactive'),
    ]
    status = models.CharField(
        max_length=35,
        choices=STATUS_CHOICES,
        default=ENABLED
    )
