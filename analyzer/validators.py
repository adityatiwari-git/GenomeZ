import re


DNA_BASES = {"A", "T", "G", "C"}
RNA_BASES = {"A", "U", "G", "C"}
VALID_BASES = DNA_BASES | RNA_BASES


def validate_sequence(sequence):
    """Clean a sequence, check its bases, and identify DNA or RNA."""
    if not sequence:
        return {"valid": False, "message": "Sequence is empty."}

    sequence = re.sub(r"\s+", "", sequence.upper())
    invalid_bases = sorted(
        {base for base in sequence if base not in VALID_BASES}
    )

    if invalid_bases:
        return {
            "valid": False,
            "sequence": sequence,
            "message": "Invalid sequence.",
            "invalid": invalid_bases,
        }

    has_t = "T" in sequence
    has_u = "U" in sequence

    if has_t and has_u:
        return {
            "valid": False,
            "sequence": sequence,
            "message": (
                "Sequence contains both T and U. Mixed DNA/RNA sequences "
                "are not supported."
            ),
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
    gc_count = counts["G"] + counts["C"]

    if sequence_type == "DNA":
        other_count = counts["A"] + counts["T"]
        other_name = "AT"
    else:
        other_count = counts["A"] + counts["U"]
        other_name = "AU"

    return {
        "valid": True,
        "sequence": sequence,
        "type": sequence_type,
        "length": length,
        "counts": counts,
        "gc_percent": round((gc_count / length) * 100, 2),
        "other_percent": round((other_count / length) * 100, 2),
        "other_name": other_name,
    }
