from django_filters import rest_framework as filters
from .models import Activity


class ActivityFilter(filters.FilterSet):
    from_date = filters.DateTimeFilter(label='from-date', field_name='schedule', lookup_expr='gte')
    to_date = filters.DateTimeFilter(label='to-date', field_name='schedule', lookup_expr='lte')

    class Meta:
        model = Activity
        fields = ['status']