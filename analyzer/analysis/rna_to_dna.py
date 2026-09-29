def rna_to_dna(sequence):
    """Convert an RNA sequence into DNA by replacing U with T."""
    return sequence.upper().replace("U", "T")
