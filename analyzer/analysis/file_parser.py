def parse_uploaded_file(uploaded_file):
    """Read a FASTA, FA, or plain-text upload and return its sequence."""
    content = uploaded_file.read().decode("utf-8")

    if uploaded_file.name.endswith((".fasta", ".fa")):
        sequence_lines = []

        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith(">"):
                sequence_lines.append(line)

        return "".join(sequence_lines)

    return content.strip()
