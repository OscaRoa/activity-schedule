from datetime import timedelta
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from .models import Activity, Survey
from .filter_classes import ActivityFilter
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import (
    CancelActivitySerializer,
    CreateActivitySerializer,
    ListActivitySerializer,
    RescheduleActivitySerializer,
    SurveySerializer
)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows  CRUD operations on the Activity model
    """
    queryset = Activity.objects.all()
    serializer_class = ListActivitySerializer
    action_custom_serializers = {  # Custom serializer mapping
        'create': CreateActivitySerializer,
        'partial_update': RescheduleActivitySerializer,
        'cancel': CancelActivitySerializer
    }
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter, ]
    filterset_class = ActivityFilter
    ordering_fields = ['status', 'schedule']

    def get_queryset(self):
        if self.action == 'list' and len(self.request.query_params) == 0:
            now = timezone.now()
            return Activity.objects.filter(
                schedule__range=[now - timedelta(days=3), now + timedelta(days=14)]
            )
        return super().get_queryset()

    def get_serializer_class(self):
        # Check if attribute exists, then get the proper serializer based on the action
        if hasattr(self, 'action_custom_serializers'):
            return self.action_custom_serializers.get(self.action, self.serializer_class)
        return super(ActivityViewSet, self).get_serializer_class()

    @action(detail=True, methods=['patch'], url_path='cancel', url_name='cancel')
    def cancel(self, request, *args, **kwargs):
        activity = self.get_object()
        serializer = self.get_serializer(activity, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


class RetrieveSurvey(viewsets.ReadOnlyModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
