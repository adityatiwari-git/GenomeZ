def generate_fasta(header, sequence):
    """Create a FASTA-formatted string from a header and sequence."""
    sequence = sequence.replace("\n", "").replace(" ", "")
    lines = [f">{header}"]

    # FASTA sequences are commonly wrapped to a fixed line length.
    for start in range(0, len(sequence), 70):
        lines.append(sequence[start:start + 70])

    return "\n".join(lines)
