from django.test import TestCase
from django.urls import reverse

from .views import analyze_protein, clean_sequence, validate_protein


class ProteomicsTests(TestCase):
    """Basic tests for the protein analyzer."""

    def test_proteomics_page(self):
        response = self.client.get(reverse("proteomics"))
        self.assertEqual(response.status_code, 200)

    def test_clean_sequence_removes_fasta_header(self):
        sequence = clean_sequence(">test\nMKWVTFISLL\n")
        self.assertEqual(sequence, "MKWVTFISLL")

    def test_valid_protein(self):
        result = validate_protein("MKWVTFIS")
        self.assertTrue(result["valid"])
        self.assertEqual(result["length"], 8)

    def test_invalid_protein(self):
        # Z is not one of the standard amino-acid letters accepted by GenomeZ.
        result = validate_protein("MKZVTF")
        self.assertFalse(result["valid"])
        self.assertIn("Z", result["invalid"])

    def test_protein_analysis(self):
        result = analyze_protein("AAAA")
        self.assertEqual(result["length"], 4)
        self.assertEqual(result["composition"]["A"], 4)
        self.assertGreater(result["molecular_weight"], 0)
