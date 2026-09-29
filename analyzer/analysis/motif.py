def find_motif(sequence, motif):
    """Find all occurrences of a specific motif, including overlaps."""
    sequence = sequence.upper()
    motif = motif.upper().strip()
    positions = []

    for index in range(len(sequence) - len(motif) + 1):
        if sequence[index:index + len(motif)] == motif:
            positions.append(index + 1)

    return {
        "Motif": motif,
        "Matches": len(positions),
        "Positions": positions,
    }


def discover_motifs(sequence, min_length=3, max_length=8, min_occurrences=2):
    """Discover every repeated exact substring in the requested length range."""
    sequence = sequence.upper()
    length = len(sequence)

    min_length = max(1, int(min_length))
    max_length = min(length, int(max_length))
    min_occurrences = max(2, int(min_occurrences))

    discovered = []

    for motif_length in range(min_length, max_length + 1):
        counts = {}
        positions = {}

        for start in range(length - motif_length + 1):
            motif = sequence[start:start + motif_length]
            counts[motif] = counts.get(motif, 0) + 1
            positions.setdefault(motif, []).append(start + 1)

        for motif, count in counts.items():
            if count >= min_occurrences:
                discovered.append(
                    {
                        "motif": motif,
                        "length": motif_length,
                        "matches": count,
                        "positions": positions[motif],
                    }
                )

    discovered.sort(key=lambda item: (-item["length"], -item["matches"], item["motif"]))
    return discovered
