"""
GenomeZ
GC Content Module
"""


def gc_content(sequence):

    sequence = sequence.upper()

    length = len(sequence)

    g = sequence.count("G")
    c = sequence.count("C")

    gc = g + c
    at_or_au = length - gc

    gc_percent = round((gc / length) * 100, 2)
    other_percent = round((at_or_au / length) * 100, 2)

    return {
        "Length": length,
        "GC Count": gc,
        "GC %": gc_percent,
        "Other %": other_percent,
    }