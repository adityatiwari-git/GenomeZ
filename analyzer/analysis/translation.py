"""
GenomeZ
Protein Translation Module
"""

CODON_TABLE = {
    # Phenylalanine
    "UUU": "F", "UUC": "F",

    # Leucine
    "UUA": "L", "UUG": "L",
    "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",

    # Isoleucine
    "AUU": "I", "AUC": "I", "AUA": "I",

    # Methionine (Start)
    "AUG": "M",

    # Valine
    "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",

    # Serine
    "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
    "AGU": "S", "AGC": "S",

    # Proline
    "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",

    # Threonine
    "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",

    # Alanine
    "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",

    # Tyrosine
    "UAU": "Y", "UAC": "Y",

    # Histidine
    "CAU": "H", "CAC": "H",

    # Glutamine
    "CAA": "Q", "CAG": "Q",

    # Asparagine
    "AAU": "N", "AAC": "N",

    # Lysine
    "AAA": "K", "AAG": "K",

    # Aspartic Acid
    "GAU": "D", "GAC": "D",

    # Glutamic Acid
    "GAA": "E", "GAG": "E",

    # Cysteine
    "UGU": "C", "UGC": "C",

    # Tryptophan
    "UGG": "W",

    # Arginine
    "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGA": "R", "AGG": "R",

    # Glycine
    "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G",

    # Stop
    "UAA": "*",
    "UAG": "*",
    "UGA": "*",
}


def translate(sequence, sequence_type):
    """
    Translate DNA/RNA into a protein sequence.
    """

    sequence = sequence.upper()

    if sequence_type == "DNA":
        sequence = sequence.replace("T", "U")

    protein = []
    codons_processed = 0
    stop_found = False

    for i in range(0, len(sequence) - 2, 3):

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
        "Stop Codon": "Yes" if stop_found else "No"
    }