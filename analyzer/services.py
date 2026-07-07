from .analysis.dna_to_rna import dna_to_rna
from .analysis.rna_to_dna import rna_to_dna
from .analysis.complement import complement
from .analysis.reverse_complement import reverse_complement
from .analysis.gc_content import gc_content
from .analysis.atgc_count import atgc_count

# Future imports
# from .analysis.gc_content import gc_content
# from .analysis.complement import complement


def run_selected_analysis(sequence, sequence_type, selected_tools):

    results = {}

    for tool in selected_tools:

        if tool == "dna_to_rna":

            if sequence_type != "DNA":
                results["DNA → RNA"] = "❌ Input must be a DNA sequence."
            else:
                results["DNA → RNA"] = dna_to_rna(sequence)

        elif tool == "rna_to_dna":

            if sequence_type != "RNA":
                results["RNA → DNA"] = "❌ Input must be an RNA sequence."
            else:
                results["RNA → DNA"] = rna_to_dna(sequence)

        elif tool == "complement":

            results["Complement"] = complement(sequence, sequence_type)

        elif tool == "reverse_complement":

            results["Reverse Complement"] = reverse_complement(
                sequence, sequence_type)

        elif tool == "gc_content":

            gc = gc_content(sequence)

            results["GC Content"] = (
                f"GC:{gc['GC %']}%|"
                f"Other:{gc['Other%']}%")

        elif tool == "atgc_count":
            counts = atgc_count(sequence)

            if sequence_type == "DNA":

                results["Base Composition"] = (
                f"A:{counts['A']}  "
                f"T:{counts['T']}  "
                f"G:{counts['G']}  "
                f"C:{counts['C']}")

            else:

                results["Base Composition"] = (
                f"A:{counts['A']}  "
                f"U:{counts['U']}  "
                f"G:{counts['G']}  "
                f"C:{counts['C']}")
        
        
    return results