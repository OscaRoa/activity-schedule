from datetime import datetime, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.activities.models import Activity
from apps.properties.models import Property
from apps.activities.serializers import ActivitySerializer


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

    fixtures = ["data"]

    def setUp(self) -> None:
        self.scheduled_activity = Activity.objects.get(pk=1)
        self.enabled_property = Property.objects.get(pk=1)
        self.disabled_property = Property.objects.get(pk=2)
        self.other_property = Property.objects.get(pk=3)
        return super().setUp()

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
            "property": self.disabled_property.pk,
            "schedule": datetime.now() + timedelta(days=3),
            "title": "An activity",
            "status": "a"
        }
        response = self.client.post(url, data)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertEqual(Activity.objects.count(), 1)

    def test_activity_creation_same_schedule_colition(self):
        """Test the creation of an activity with an already used schedule
        on a property.
        """
        url = reverse('activity-list')
        data = {
            "property": self.scheduled_activity.property.id,
            "schedule": self.scheduled_activity.schedule,
            "title": "An activity",
            "status": "a"
        }
        response = self.client.post(url, data)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertEqual(Activity.objects.count(), 1)

    def test_activity_creation_schedule_colition(self):
        """Test the creation of an activity with a timedelta < 60 minutes of
        a previous one on the same property.
        - E.g.
            - Schedule A: 2021-09-15 12:00:00
                - Invalid new schedule: 2021-09-15 12:59:00
                - Valid new schedule: 2021-09-15 13:00:00
        """
        url = reverse('activity-list')
        data = {
            "property": self.scheduled_activity.property.id,
            "schedule": self.scheduled_activity.schedule + timedelta(minutes=59),
            "title": "An activity",
            "status": "a"
        }
        response = self.client.post(url, data)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertEqual(Activity.objects.count(), 1)

    def test_update_activity_property(self):
        """Test updating the property of an existing activity.
        """
        url = reverse('activity-detail', args=[self.scheduled_activity.id])
        data = {
            "property": self.other_property.pk
        }
        response = self.client.patch(url, data)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_update_activity_schedule(self):
        """Test updating the schedule of a property.
        """
        url = reverse('activity-detail', args=[self.scheduled_activity.id])
        data = {
            "schedule": self.scheduled_activity.schedule + timedelta(minutes=60)
        }
        response = self.client.patch(url, data)
        self.assertTrue(status.is_success(response.status_code))

    def test_update_canceled_activity(self):
        """Test updating a property with the canceled status.
        """
        self.scheduled_activity.status = 'c'
        self.scheduled_activity.save()
        url = reverse('activity-detail', args=[self.scheduled_activity.id])
        data = {
            "schedule": self.scheduled_activity.schedule + timedelta(minutes=60)
        }
        response = self.client.patch(url, data)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_cancel_activity(self):
        """Test updating the activity status to canceled.
        """
        url = reverse('activity-detail', args=[self.scheduled_activity.id])
        data = {
            "status": "c"
        }
        response = self.client.patch(url, data)
        self.assertTrue(status.is_success(response.status_code))

    def test_list_activities(self):
        """Test listing all the activities.
        """
        activities = Activity.objects.all()
        serialized = ActivitySerializer(activities, many=True)
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.data, serialized.data)
        self.assertTrue(status.is_success(response.status_code))
