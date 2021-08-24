from datetime import timedelta
from .models import Activity
from rest_framework import serializers


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

    def validate_property(self, property):
        """Validate if the assigned propery is disabled.

        Args:
            property (Property): A property object
        """
        if property.status == "d":
            raise serializers.ValidationError("Can't assign disabled property to activity.")
        return property

    def validate(self, data):
        try:
            # Queryset to filter any activity in the window of +-59 minutes
            # as activities last an hour.
            if Activity.objects.filter(
                property=data['property'],
                schedule__range=[
                    data['schedule']-timedelta(minutes=59),
                    data['schedule']+timedelta(minutes=59)
                ]
            ).exists():
                raise serializers.ValidationError("Schedule already in use.")
        except KeyError:
            pass
        return data
