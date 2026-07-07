"""
GenomeZ
ATGC Count Module
"""


def atgc_count(sequence):

    sequence = sequence.upper()

    return {
        "A": sequence.count("A"),
        "T": sequence.count("T"),
        "U": sequence.count("U"),
        "G": sequence.count("G"),
        "C": sequence.count("C"),
        "Length": len(sequence),
    }