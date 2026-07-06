import re

VALID_DNA = {"A", "T", "G", "C"}


def validate_dna(sequence):
    """
    Validate a DNA sequence and return useful statistics.

    Returns:
        {
            "valid": bool,
            "sequence": str,
            "length": int,
            "counts": dict,
            "gc_percent": float,
            "at_percent": float,
            "type": str,
            "invalid": list,
            "message": str
        }
    """

    # Empty input
    if not sequence:
        return {
            "valid": False,
            "message": "Sequence is empty."
        }

    # Remove spaces, tabs and newlines
    sequence = re.sub(r"\s+", "", sequence.upper())

    # Find invalid characters
    invalid = sorted(set([char for char in sequence if char not in VALID_DNA]))

    if invalid:
        return {
            "valid": False,
            "sequence": sequence,
            "invalid": invalid,
            "message": "Invalid DNA sequence."
        }

    # Base counts
    counts = {
        "A": sequence.count("A"),
        "T": sequence.count("T"),
        "G": sequence.count("G"),
        "C": sequence.count("C"),
    }

    length = len(sequence)

    gc = counts["G"] + counts["C"]
    at = counts["A"] + counts["T"]

    gc_percent = round((gc / length) * 100, 2)
    at_percent = round((at / length) * 100, 2)

    return {
        "valid": True,
        "sequence": sequence,
        "length": length,
        "counts": counts,
        "gc_percent": gc_percent,
        "at_percent": at_percent,
        "type": "DNA",
    }