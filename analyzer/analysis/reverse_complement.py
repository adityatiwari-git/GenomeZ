from .complement import complement


def reverse_complement(sequence, sequence_type):
    """Return the reverse complement of a DNA or RNA sequence."""
    return complement(sequence, sequence_type)[::-1]
