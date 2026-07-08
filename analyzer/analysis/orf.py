"""
GenomeZ
Open Reading Frame (ORF) Finder
"""

STOP_CODONS = {
    "DNA": {"TAA", "TAG", "TGA"},
    "RNA": {"UAA", "UAG", "UGA"}
}


def find_orfs(sequence, sequence_type):

    sequence = sequence.upper()

    start_codon = "ATG" if sequence_type == "DNA" else "AUG"
    stop_codons = STOP_CODONS[sequence_type]

    orfs = []

    i = 0

    while i <= len(sequence) - 3:

        codon = sequence[i:i + 3]

        if codon == start_codon:

            j = i + 3

            while j <= len(sequence) - 3:

                stop = sequence[j:j + 3]

                if stop in stop_codons:

                    orfs.append({
                        "start": i + 1,
                        "end": j + 3,
                        "length": j + 3 - i,
                        "sequence": sequence[i:j + 3]
                    })

                    break

                j += 3

        i += 1

    return orfs