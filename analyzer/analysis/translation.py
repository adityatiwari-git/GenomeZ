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

    if sequence_type == "DNA":
        sequence = sequence.replace("T", "U")

    start = sequence.find("AUG")

    if start == -1:
        return {
            "Protein": "",
            "Codons": 0,
            "Stop Codon": "No",
            "Start Found": "No",
        }

    protein = []
    codons_processed = 0
    stop_found = False

    for i in range(start, len(sequence) - 2, 3):
        codon = sequence[i:i + 3]
        amino = CODON_TABLE.get(codon, "X")
        codons_processed += 1

        if amino == "*":
            stop_found = True
            break

        protein.append(amino)

    return {
        "Protein": "".join(protein),
        "Codons": codons_processed,
        "Stop Codon": "Yes" if stop_found else "No",
        "Start Found": "Yes",
    }
