def generate_fasta(header, sequence):

    sequence = sequence.replace("\n", "").replace(" ", "")

    lines = [f">{header}"]

    for i in range(0, len(sequence), 70):
        lines.append(sequence[i:i+70])

    return "\n".join(lines)