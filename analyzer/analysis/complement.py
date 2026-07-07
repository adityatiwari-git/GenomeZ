"""
GenomeZ
Complement Sequence Module
"""


DNA_COMPLEMENT = {
    "A": "T",
    "T": "A",
    "G": "C",
    "C": "G",
}

RNA_COMPLEMENT = {
    "A": "U",
    "U": "A",
    "G": "C",
    "C": "G",
}


def complement(sequence, sequence_type):
    """
    Generate the complement of a DNA or RNA sequence.
    """

    sequence = sequence.upper()

    mapping = DNA_COMPLEMENT if sequence_type == "DNA" else RNA_COMPLEMENT

    return "".join(mapping[base] for base in sequence)