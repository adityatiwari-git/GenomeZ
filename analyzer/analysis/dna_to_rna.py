"""
GenomeZ
DNA → RNA Conversion Module
"""


def dna_to_rna(sequence):
    """
    Convert a DNA sequence into an RNA sequence.

    Parameters:
        sequence (str): Valid DNA sequence

    Returns:
        str: RNA sequence
    """

    sequence = sequence.upper()

    return sequence.replace("T", "U")