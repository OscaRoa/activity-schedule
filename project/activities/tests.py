# from django.urls import reverse
# from rest_framework import status
from rest_framework.test import APITestCase


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
        return super().setUp()

    def test_dummy(self) -> None:
        self.assertEqual(1, 1)
