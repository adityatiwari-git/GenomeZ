import re

DNA_BASES = {"A", "T", "G", "C"}
RNA_BASES = {"A", "U", "G", "C"}
VALID_BASES = {"A", "T", "G", "C", "U"}


def validate_sequence(sequence):
    """
    Validate and identify whether the sequence is DNA or RNA.
    """

    if not sequence:
        return {
            "valid": False,
            "message": "Sequence is empty."
        }

    # Remove spaces and newlines
    sequence = re.sub(r"\s+", "", sequence.upper())

    # Find invalid characters
    invalid = sorted(set(ch for ch in sequence if ch not in VALID_BASES))

    if invalid:
        return {
            "valid": False,
            "sequence": sequence,
            "message": "Invalid sequence.",
            "invalid": invalid
        }

    has_t = "T" in sequence
    has_u = "U" in sequence

    # DNA and RNA mixed together
    if has_t and has_u:
        return {
            "valid": False,
            "sequence": sequence,
            "message": "Sequence contains both T and U. Mixed DNA/RNA sequences are not supported."
        }

    sequence_type = "DNA" if has_t else "RNA"

    counts = {
        "A": sequence.count("A"),
        "T": sequence.count("T"),
        "G": sequence.count("G"),
        "C": sequence.count("C"),
        "U": sequence.count("U"),
    }

    length = len(sequence)

    gc = counts["G"] + counts["C"]

    if sequence_type == "DNA":
        other = counts["A"] + counts["T"]
        other_name = "AT"
    else:
        other = counts["A"] + counts["U"]
        other_name = "AU"

    gc_percent = round((gc / length) * 100, 2)
    other_percent = round((other / length) * 100, 2)

    return {
        "valid": True,
        "sequence": sequence,
        "type": sequence_type,
        "length": length,
        "counts": counts,
        "gc_percent": gc_percent,
        "other_percent": other_percent,
        "other_name": other_name,
    }