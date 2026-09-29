from .complement import complement


def reverse_complement(sequence, sequence_type):
    """Return the reverse complement of a DNA or RNA sequence."""
    complemented_sequence = complement(sequence, sequence_type)
    return complemented_sequence[::-1]
