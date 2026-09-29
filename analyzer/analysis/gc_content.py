def gc_content(sequence):
    """Calculate GC count and GC percentage for a sequence."""
    sequence = sequence.upper()
    length = len(sequence)

    gc_count = sequence.count("G") + sequence.count("C")
    other_count = length - gc_count

    return {
        "Length": length,
        "GC Count": gc_count,
        "GC %": round((gc_count / length) * 100, 2),
        "Other %": round((other_count / length) * 100, 2),
    }
