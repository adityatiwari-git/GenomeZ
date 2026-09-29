CODON_TABLE = {
    "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
    "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
    "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
    "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
    "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
    "AGU": "S", "AGC": "S",
    "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "UAU": "Y", "UAC": "Y", "CAU": "H", "CAC": "H",
    "CAA": "Q", "CAG": "Q", "AAU": "N", "AAC": "N",
    "AAA": "K", "AAG": "K", "GAU": "D", "GAC": "D",
    "GAA": "E", "GAG": "E", "UGU": "C", "UGC": "C",
    "UGG": "W",
    "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGA": "R", "AGG": "R",
    "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G",
    "UAA": "*", "UAG": "*", "UGA": "*",
}


def translate(sequence, sequence_type):
    """Translate a DNA or RNA sequence from its first start codon."""
    sequence = sequence.upper()

    # The codon table uses RNA bases, so convert DNA first.
    if sequence_type == "DNA":
        sequence = sequence.replace("T", "U")

    start_index = sequence.find("AUG")

    if start_index == -1:
        return {
            "Protein": "",
            "Codons": 0,
            "Stop Codon": "No",
            "Start Found": "No",
        }

    protein = []
    codons_processed = 0
    stop_found = False

    for index in range(start_index, len(sequence) - 2, 3):
        codon = sequence[index:index + 3]
        amino_acid = CODON_TABLE.get(codon, "X")
        codons_processed += 1

        if amino_acid == "*":
            stop_found = True
            break

        protein.append(amino_acid)

    return {
        "Protein": "".join(protein),
        "Codons": codons_processed,
        "Stop Codon": "Yes" if stop_found else "No",
        "Start Found": "Yes",
    }
