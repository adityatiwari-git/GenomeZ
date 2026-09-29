from .analysis.atgc_count import atgc_count
from .analysis.complement import complement
from .analysis.dna_to_rna import dna_to_rna
from .analysis.gc_content import gc_content
from .analysis.identification import identify_sequence
from .analysis.motif import find_motif
from .analysis.orf import find_orfs
from .analysis.reverse_complement import reverse_complement
from .analysis.rna_to_dna import rna_to_dna
from .analysis.translation import translate


def run_selected_analysis(sequence, sequence_type, selected_tools, motif=""):
    """Run the tools selected by the user and collect their results."""
    results = {}

    for tool in selected_tools:
        if tool == "dna_to_rna":
            if sequence_type != "DNA":
                results["DNA → RNA"] = {
                    "display": "❌ Input must be a DNA sequence.",
                    "raw": None,
                    "format": "text",
                }
            else:
                rna = dna_to_rna(sequence)
                results["DNA → RNA"] = {
                    "display": rna,
                    "raw": rna,
                    "format": "sequence",
                }

        elif tool == "rna_to_dna":
            if sequence_type != "RNA":
                results["RNA → DNA"] = {
                    "display": "❌ Input must be an RNA sequence.",
                    "raw": None,
                    "format": "text",
                }
            else:
                dna = rna_to_dna(sequence)
                results["RNA → DNA"] = {
                    "display": dna,
                    "raw": dna,
                    "format": "sequence",
                }

        elif tool == "complement":
            if sequence_type == "PROTEIN":
                results["Complement"] = {
                    "display": "❌ Complement is only available for DNA/RNA sequences.",
                    "raw": None,
                    "format": "text",
                }
            else:
                result = complement(sequence, sequence_type)
                results["Complement"] = {
                    "display": result,
                    "raw": result,
                    "format": "sequence",
                }

        elif tool == "reverse_complement":
            if sequence_type == "PROTEIN":
                results["Reverse Complement"] = {
                    "display": "❌ Reverse Complement is only available for DNA/RNA sequences.",
                    "raw": None,
                    "format": "text",
                }
            else:
                result = reverse_complement(sequence, sequence_type)
                results["Reverse Complement"] = {
                    "display": result,
                    "raw": result,
                    "format": "sequence",
                }

        elif tool == "gc_content":
            gc_result = gc_content(sequence)
            display = (
                f"GC: {gc_result['GC %']}%\n"
                f"Other: {gc_result['Other %']}%"
            )

            results["GC Content"] = {
                "display": display,
                "raw": None,
                "format": "text",
            }

        elif tool == "atgc_count":
            counts = atgc_count(sequence)

            if sequence_type == "DNA":
                display = (
                    f"A: {counts['A']}\n"
                    f"T: {counts['T']}\n"
                    f"G: {counts['G']}\n"
                    f"C: {counts['C']}"
                )
            else:
                display = (
                    f"A: {counts['A']}\n"
                    f"U: {counts['U']}\n"
                    f"G: {counts['G']}\n"
                    f"C: {counts['C']}"
                )

            results["Base Composition"] = {
                "display": display,
                "raw": None,
                "format": "text",
            }

        elif tool == "translation":
            translation = translate(sequence, sequence_type)

            if translation["Start Found"] == "No":
                display = "No start codon (ATG/AUG) found."
            else:
                display = (
                    f"Protein: {translation['Protein']}\n"
                    f"Codons: {translation['Codons']}\n"
                    "Start Codon: Yes\n"
                    f"Stop Codon: {translation['Stop Codon']}"
                )

            results["Protein Translation"] = {
                "display": display,
                "raw": translation["Protein"] or None,
                "format": "sequence" if translation["Protein"] else "text",
            }

        elif tool == "motif":
            if not motif:
                results["Motif Finder"] = {
                    "display": "❌ Please enter a motif.",
                    "raw": None,
                    "format": "text",
                }
            else:
                motif_result = find_motif(sequence, motif)

                if motif_result["Matches"] == 0:
                    display = (
                        f"Motif: {motif_result['Motif']}\n"
                        "No matches found."
                    )
                else:
                    positions = ", ".join(
                        map(str, motif_result["Positions"])
                    )
                    display = (
                        f"Motif: {motif_result['Motif']}\n"
                        f"Matches: {motif_result['Matches']}\n"
                        f"Positions: {positions}"
                    )

                results["Motif Finder"] = {
                    "display": display,
                    "raw": None,
                    "format": "text",
                }

        elif tool == "orf":
            orfs = find_orfs(sequence, sequence_type)

            if not orfs:
                results["ORF Finder"] = {
                    "display": "No ORFs found.",
                    "raw": None,
                    "format": "text",
                }
            else:
                output = ""

                for index, orf in enumerate(orfs, start=1):
                    output += (
                        f"ORF {index}\n"
                        f"Frame : {orf['frame']}\n"
                        f"Start : {orf['start']}\n"
                        f"End : {orf['end']}\n"
                        f"Length : {orf['length']} bp\n"
                        f"Sequence : {orf['sequence']}\n\n"
                    )

                results["ORF Finder"] = {
                    "display": output,
                    "raw": None,
                    "format": "text",
                }

        elif tool == "blast":
            if sequence_type != "DNA":
                results["Sequence Identification"] = {
                    "display": (
                        "Sequence identification currently uses NCBI BLASTN "
                        "and requires a DNA sequence."
                    ),
                    "raw": None,
                    "format": "text",
                }
            else:
                identification = identify_sequence(sequence)

                if identification["error"]:
                    display = f"Identification error: {identification['error']}"
                else:
                    display = identification.get(
                        "message",
                        "NCBI BLAST request submitted.",
                    )

                results["Sequence Identification"] = {
                    "display": display,
                    "raw": None,
                    "format": "text",
                }

    return results
