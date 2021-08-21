from django.db import models


class CreatedBaseModel(models.Model):
    """Abstract model with the created_at field.
    """
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class CreateUpdatedBaseModel(CreatedBaseModel):
    """Abstract model with the created and updated at fields.
    """
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
