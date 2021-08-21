from .models import Activity
from rest_framework import serializers


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activity
        fields = ['property', 'schedule', 'title', 'created_at', 'updated_at', 'status']
