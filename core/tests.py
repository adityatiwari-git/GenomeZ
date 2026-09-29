from django.test import TestCase


class HomePageTests(TestCase):
    """Tests for the public GenomeZ homepage."""

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/home.html")
