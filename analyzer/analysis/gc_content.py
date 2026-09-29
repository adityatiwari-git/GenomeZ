def gc_content(sequence):
    sequence = sequence.upper()
    length = len(sequence)

    gc = sequence.count("G") + sequence.count("C")
    other = length - gc

    return {
        "Length": length,
        "GC Count": gc,
        "GC %": round((gc / length) * 100, 2),
        "Other %": round((other / length) * 100, 2),
    }
