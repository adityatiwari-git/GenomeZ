"""
GenomeZ
RNA → DNA Conversion Module
"""


def rna_to_dna(sequence):
    """
    Convert RNA sequence into DNA sequence.
    """

    sequence = sequence.upper()

    return sequence.replace("U", "T")