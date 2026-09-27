from django.test import TestCase

from .validators import validate_sequence
from .analysis.dna_to_rna import dna_to_rna
from .analysis.rna_to_dna import rna_to_dna
from .analysis.gc_content import gc_content
from .analysis.atgc_count import atgc_count
from .analysis.complement import complement
from .analysis.reverse_complement import reverse_complement
from .analysis.translation import translate
from .analysis.motif import find_motif
from .analysis.orf import find_orfs


class AnalyzerTests(TestCase):

    def test_analyzer_is_public(self):
        response = self.client.get("/analyzer/")
        self.assertEqual(response.status_code, 200)

    def test_guest_can_use_free_tool(self):
        response = self.client.post(
            "/analyzer/",
            {"sequence": "ATGC", "analysis": ["gc_content"]},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "GC Content")

    def test_guest_is_redirected_for_premium_tool(self):
        response = self.client.post(
            "/analyzer/",
            {"sequence": "ATGC", "analysis": ["blast"]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_dna_validation(self):
        result = validate_sequence("ATGC")
        self.assertTrue(result["valid"])
        self.assertEqual(result["type"], "DNA")
        self.assertEqual(result["length"], 4)

    def test_rna_validation(self):
        result = validate_sequence("AUGC")
        self.assertTrue(result["valid"])
        self.assertEqual(result["type"], "RNA")

    def test_invalid_sequence(self):
        result = validate_sequence("ATGX")
        self.assertFalse(result["valid"])

    def test_dna_to_rna(self):
        self.assertEqual(dna_to_rna("ATGC"), "AUGC")

    def test_rna_to_dna(self):
        self.assertEqual(rna_to_dna("AUGC"), "ATGC")

    def test_gc_content(self):
        result = gc_content("GCGCAA")
        self.assertEqual(result["GC Count"], 4)
        self.assertEqual(result["GC %"], 66.67)

    def test_base_count(self):
        result = atgc_count("ATGCA")
        self.assertEqual(result["A"], 2)
        self.assertEqual(result["T"], 1)
        self.assertEqual(result["G"], 1)
        self.assertEqual(result["C"], 1)

    def test_complement(self):
        self.assertEqual(complement("ATGC", "DNA"), "TACG")
        self.assertEqual(complement("AUGC", "RNA"), "UACG")

    def test_reverse_complement(self):
        self.assertEqual(reverse_complement("ATGC", "DNA"), "GCAT")
        self.assertEqual(reverse_complement("AUGC", "RNA"), "GCAU")

    def test_translation(self):
        result = translate("CCCATGGCCATGTAA", "DNA")
        self.assertEqual(result["Protein"], "MAM")
        self.assertEqual(result["Start Found"], "Yes")
        self.assertEqual(result["Stop Codon"], "Yes")

    def test_translation_without_start(self):
        result = translate("GCCGCCGCC", "DNA")
        self.assertEqual(result["Start Found"], "No")

    def test_motif(self):
        result = find_motif("ATATAT", "ATA")
        self.assertEqual(result["Matches"], 2)
        self.assertEqual(result["Positions"], [1, 3])

    def test_orf(self):
        result = find_orfs("CCCATGAAATAG", "DNA")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["start"], 4)
        self.assertEqual(result[0]["end"], 12)
        self.assertEqual(result[0]["frame"], 1)
