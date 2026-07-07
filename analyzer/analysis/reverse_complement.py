"""
GenomeZ
Reverse Complement Module
"""

from .complement import complement


def reverse_complement(sequence, sequence_type):
    """
    Generate reverse complement of DNA/RNA.
    """

    return complement(sequence, sequence_type)[::-1]