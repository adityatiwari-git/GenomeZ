from django.test import TestCase


class ProteomicsTests(TestCase):

    def test_proteomics_page(self):
        response = self.client.get("/proteomics/")
        self.assertEqual(response.status_code, 200)
