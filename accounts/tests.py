from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountsTests(TestCase):

    def test_signup_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
            },
        )

        self.assertRedirects(response, reverse("analyzer"))
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_login(self):
        User.objects.create_user(
            username="testuser",
            password="StrongPassword123!",
        )

        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "StrongPassword123!",
            },
        )

        self.assertRedirects(response, reverse("analyzer"))
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_logout(self):
        user = User.objects.create_user(
            username="testuser",
            password="StrongPassword123!",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("logout"))

        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)
