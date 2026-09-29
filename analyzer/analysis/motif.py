def find_motif(sequence, motif):
    """Find all occurrences of a motif, including overlapping matches."""
    sequence = sequence.upper()
    motif = motif.upper()
    positions = []

    # Move one base at a time so overlapping matches are also found.
    for index in range(len(sequence) - len(motif) + 1):
        if sequence[index:index + len(motif)] == motif:
            positions.append(index + 1)

    return {
        "Motif": motif,
        "Matches": len(positions),
        "Positions": positions,
    }
