"""
GenomeZ
Motif Finder
"""


def find_motif(sequence, motif):
    """
    Find all occurrences of a motif (including overlapping matches).
    """

    sequence = sequence.upper()
    motif = motif.upper()

    positions = []

    for i in range(len(sequence) - len(motif) + 1):

        if sequence[i:i + len(motif)] == motif:
            positions.append(i + 1)   # 1-based indexing

    return {
        "Motif": motif,
        "Matches": len(positions),
        "Positions": positions
    }