from activities.models import Activity
from rest_framework import viewsets
from activities.serializers import ActivitySerializer


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows  CRUD operations on the Activity model
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
