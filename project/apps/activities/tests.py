from datetime import datetime, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.activities.models import Activity
from apps.properties.models import Property
from apps.activities.views import ActivityViewSet


class ActivityTests(APITestCase):
    """Test case class to validate project's logic requirements.

    Creation:
        - Properties must be active.
        - Schedule time must be available for a given property
        - Activities last up to an hour

    Update:
        - Reschedule
            - Only the schedule time can be changed, not the property.
            - Canceled activities can't be rescheduled.
        - Cancel
            - Activity status is set to canceled.

    List:
        - Base filtering: now - 3 days <= schedule <= now + 2 weeks
        - Survey is a hyperlinked key in the serializer
        - Property is serialized inside an activity
        - Condition:
            - 'Pendiente a realizar': active status AND schedule >= now
            - 'Atrasada': active status AND schedule <= now
            - 'Finalizada': done status
        - Fields included:
            id, schedule, title, created_at, status and the ones above.
    """

    # 1 property enabled, 1 disabled and an scheduled activity on 02/09/21
    fixtures = ["data"]

    def test_root(self) -> None:
        """Test if the API root responds correctly.
        """
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_activity_creation_disabled_property(self):
        """Test the creation of an activity with a disabled property.
        """
        url = reverse('activity-list')
        data = {
            "property": 2,  # Disabled property
            "schedule": datetime.now() + timedelta(days=3),
            "title": "An activity",
            "status": "a"
        }
        response = self.client.post(url, data)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertEqual(Activity.objects.count(), 1)
