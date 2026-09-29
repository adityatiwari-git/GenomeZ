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
    """Return the complement of a DNA or RNA sequence."""
    sequence = sequence.upper()

    if sequence_type == "DNA":
        bases = DNA_COMPLEMENT
    else:
        bases = RNA_COMPLEMENT

    return "".join(bases[base] for base in sequence)
