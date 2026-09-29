def dna_to_rna(sequence):
    """Convert a DNA sequence into an RNA sequence."""
    sequence = sequence.upper()
    return sequence.replace("T", "U")
