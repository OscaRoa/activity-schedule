from django.db import models
from django.contrib.postgres.fields import JSONField


class Property(models.Model):
    title = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=35)


class Activity(models.Model):
    property = models.ForeignKey(
        Property,
        related_name="property_id",
        on_delete=models.CASCADE,
    )
    schedule = models.DateTimeField()
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=35)


class Survey(models.Model):
    activity = models.OneToOneField(
        Activity,
        on_delete=models.CASCADE,
    )
    answers = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
