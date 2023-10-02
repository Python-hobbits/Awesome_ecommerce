from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class UserProfileTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_profile_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("user_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

    def test_user_profile_update_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("user_profile_edit"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_profile_edit.html")

    def test_user_profile_update_view_post(self):
        self.client.login(username="testuser", password="testpassword")
        updated_data = {"first_name": "Updated", "last_name": "User"}
        response = self.client.post(reverse("user_profile_edit"), data=updated_data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, updated_data["first_name"])
        self.assertEqual(self.user.last_name, updated_data["last_name"])
