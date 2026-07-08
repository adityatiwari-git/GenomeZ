from .analysis.dna_to_rna import dna_to_rna
from .analysis.rna_to_dna import rna_to_dna
from .analysis.complement import complement
from .analysis.reverse_complement import reverse_complement
from .analysis.gc_content import gc_content
from .analysis.atgc_count import atgc_count
from .analysis.translation import translate
from .analysis.motif import find_motif
from .analysis.orf import find_orfs

# Future imports
# from .analysis.gc_content import gc_content
# from .analysis.complement import complement

def run_selected_analysis(sequence, sequence_type, selected_tools, motif=""):

    results = {}

    for tool in selected_tools:

        if tool == "dna_to_rna":

            if sequence_type != "DNA":
                results["DNA → RNA"] = "❌ Input must be a DNA sequence."
            else:
                rna = dna_to_rna(sequence)
                results["DNA → RNA"] = {
                    "display": rna,
                    "raw": rna,
                    "format": "sequence"}

        elif tool == "rna_to_dna":

            if sequence_type != "RNA":
                results["RNA → DNA"] = "❌ Input must be an RNA sequence."
            else:
                dna = rna_to_dna(sequence)

                results["RNA → DNA"] = {
                    "display": dna,
                    "raw": dna,
                    "format": "sequence"}

        elif tool == "complement":

            comp = complement(sequence, sequence_type)
            results["Complement"] = {
                "display": comp,
                "raw": comp,
                "format": "sequence"}

        elif tool == "reverse_complement":

            rev = reverse_complement(sequence, sequence_type)

            results["Reverse Complement"] = {
                "display": rev,
                "raw": rev,
                "format": "sequence"}

        elif tool == "gc_content":

            gc = gc_content(sequence)

            results["GC Content"] = {
                "display": (
                    f"GC: {gc['GC %']}%\n"
                    f"Other: {gc['Other %']}%"),
                
                "raw": None,
                "format": "text"}
            
            
            
        elif tool == "atgc_count":
            counts = atgc_count(sequence)

            if sequence_type == "DNA":

                display = (
                    f"A: {counts['A']}\n"
                    f"T: {counts['T']}\n"
                    f"G: {counts['G']}\n"
                    f"C: {counts['C']}")

            else:

                display = (
                    f"A: {counts['A']}\n"
                    f"U: {counts['U']}\n"
                    f"G: {counts['G']}\n"
                    f"C: {counts['C']}")

            results["Base Composition"] = {
                "display": display,
                "raw": None,
                "format": "text"}
        
        elif tool == "translation":
            translation = translate(sequence, sequence_type)

            results["Protein Translation"] = {
                "display": (
                    f"Protein: {translation['Protein']}\n"
                    f"Codons: {translation['Codons']}\n"
                    f"Stop Codon: {translation['Stop Codon']}"),
                    
                "raw": translation["Protein"],
                "format": "sequence"}
        
        elif tool == "motif":

            if not motif:

                results["Motif Finder"] = {
                    "display": "❌ Please enter a motif.",
                    "raw": None,
                    "format": "text"
                }

            else:

                result = find_motif(sequence, motif)

                if result["Matches"] == 0:

                    display = (
                        f"Motif: {result['Motif']}\n"
                        "No matches found."
                    )

                else:

                    positions = ", ".join(map(str, result["Positions"]))

                    display = (
                        f"Motif: {result['Motif']}\n"
                        f"Matches: {result['Matches']}\n"
                        f"Positions: {positions}"
                    )

                results["Motif Finder"] = {
                    "display": display,
                    "raw": None,
                    "format": "text"
                }
                
        elif tool == "orf":

            orfs = find_orfs(sequence, sequence_type)

            if not orfs:

                results["ORF Finder"] = {
                    "display": "No ORFs found.",
                    "raw": None,
                    "format": "text"
                }

            else:

                output = ""

                fasta_sequence = ""

                for i, orf in enumerate(orfs, start=1):

                    output += (
                        f"ORF {i}\n"
                        f"Start : {orf['start']}\n"
                        f"End : {orf['end']}\n"
                        f"Length : {orf['length']} bp\n"
                        f"Sequence : {orf['sequence']}\n\n"
                    )

                    fasta_sequence += orf["sequence"]

                results["ORF Finder"] = {
                    "display": output,
                    "raw": fasta_sequence,
                    "format": "sequence"
                }
        
        
        
    return results