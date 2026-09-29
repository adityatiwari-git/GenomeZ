def atgc_count(sequence):
    """Count the common bases and return the sequence length."""
    sequence = sequence.upper()

    return {
        "A": sequence.count("A"),
        "T": sequence.count("T"),
        "U": sequence.count("U"),
        "G": sequence.count("G"),
        "C": sequence.count("C"),
        "Length": len(sequence),
    }
