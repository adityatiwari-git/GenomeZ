def rna_to_dna(sequence):
    """Convert an RNA sequence into a DNA sequence."""
    sequence = sequence.upper()
    return sequence.replace("U", "T")
