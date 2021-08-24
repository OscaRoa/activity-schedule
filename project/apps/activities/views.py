from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
from .models import Activity
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import (
    CancelActivitySerializer,
    CreateActivitySerializer,
    ListActivitySerializer,
    RescheduleActivitySerializer
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

    def get_queryset(self):
        if self.action == 'list':
            now = timezone.now()
            return Activity.objects.filter(
                schedule__range=[now - timedelta(days=3), now + timedelta(days=14)]
            )
        return self.queryset

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
        response_data = self.serializer_class(activity).data
        return Response(data=response_data)
