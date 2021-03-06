from datetime import timedelta

from django.utils import timezone
from apps.properties.models import Property
from apps.properties.serializers import PropertySerializer
from .models import Activity, Survey
from rest_framework import serializers


class CreateActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

    def validate_property(self, property):
        """Validate if the assigned propery is disabled.

        Args:
            property (Property): A property object
        """
        if property.status == Property.DISABLED:
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


class ListActivitySerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    condition = serializers.SerializerMethodField()
    survey = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='survey-detail'
    )

    class Meta:
        model = Activity
        fields = [
            'id',
            'schedule',
            'title',
            'created_at',
            'status',
            'property',
            'condition',
            'survey'
        ]

    def get_condition(self, obj):
        now = timezone.now()
        PENDING = "Pendiente a realizar"
        DELAYED = "Atrasada"
        FINISHED = "Finalizada"
        CANCELED = "Cancelada"
        if obj.status == obj.ACTIVE and obj.schedule >= now:
            return PENDING
        elif obj.status == obj.ACTIVE and obj.schedule <= now:
            return DELAYED
        elif obj.status == obj.COMPLETED:
            return FINISHED
        else:
            return CANCELED


class BaseUpdateActivitySerializer(serializers.ModelSerializer):
    """Custom serializer lass. Raises ValidationError if an unkown
    field was sent in the request body.
    """
    class Meta:
        model = Activity

    def validate(self, data):
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                raise serializers.ValidationError("Got unknown fields: {}".format(unknown_keys))
        return data


class CancelActivitySerializer(BaseUpdateActivitySerializer):
    class Meta(BaseUpdateActivitySerializer.Meta):
        fields = ['status']


class RescheduleActivitySerializer(BaseUpdateActivitySerializer):
    class Meta(BaseUpdateActivitySerializer.Meta):
        fields = ['schedule']

    def validate_schedule(self, schedule):
        if self.instance.status == Activity.CANCELED:
            raise serializers.ValidationError("Can't reschedule canceled activity.")
        if self.instance.schedule == schedule:
            pass
        elif Activity.objects.filter(  # Catch schedule colition
                property=self.instance.property,
                schedule__range=[
                    schedule - timedelta(minutes=59),
                    schedule + timedelta(minutes=59)
                ]
            ).exists():
            raise serializers.ValidationError("Schedule already in use.")
        return schedule


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'
