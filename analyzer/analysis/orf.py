STOP_CODONS = {
    "DNA": {"TAA", "TAG", "TGA"},
    "RNA": {"UAA", "UAG", "UGA"},
}


def find_orfs(sequence, sequence_type):
    """Find open reading frames that start and end with valid codons."""
    sequence = sequence.upper()
    start_codon = "ATG" if sequence_type == "DNA" else "AUG"
    stop_codons = STOP_CODONS[sequence_type]
    orfs = []

    # Check all three possible reading frames.
    for frame in range(3):
        start_index = frame

        while start_index <= len(sequence) - 3:
            codon = sequence[start_index:start_index + 3]

            if codon == start_codon:
                end_index = start_index + 3

                while end_index <= len(sequence) - 3:
                    stop_codon = sequence[end_index:end_index + 3]

                    if stop_codon in stop_codons:
                        orfs.append({
                            "start": start_index + 1,
                            "end": end_index + 3,
                            "length": end_index + 3 - start_index,
                            "sequence": sequence[start_index:end_index + 3],
                            "frame": frame + 1,
                        })
                        break

                    end_index += 3

            start_index += 3

    return orfs
