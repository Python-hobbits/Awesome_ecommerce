from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from src.apps.user.models import UserProfile, UserAddress


class UserProfileTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.user_profile = UserProfile.objects.create(
            address=UserAddress.objects.create(
                country="Test Country",
                city="Test City",
                street="Test Street",
                building="1",
                apartment="2",
            ),
            mobile_phone="1234567890",
        )

        self.user.user_profile = self.user_profile
        self.user.save()

    def test_user_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("user_detail", args=[self.user.uuid]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/user_detail.html")

    def test_user_update_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("user_edit", args=[self.user.uuid]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/user_edit.html")
        self.assertEqual(self.user.user_profile.address.building, "1")

    def test_user_update_view_post(self):
        self.client.login(username="testuser", password="testpassword")
        updated_data = {
            "first_name": "Updated",
            "last_name": "User",
            "country": "Test Country",
            "city": "Test City",
            "street": "Test Street",
            "building": "11",
        }
        response = self.client.post(reverse("user_edit", args=[self.user.uuid]), data=updated_data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, updated_data["first_name"])
        self.assertEqual(self.user.last_name, updated_data["last_name"])
        self.assertEqual(self.user.user_profile.address.building, updated_data["building"])
