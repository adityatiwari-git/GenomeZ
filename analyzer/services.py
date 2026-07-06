from .analysis.dna_to_rna import dna_to_rna
from .analysis.rna_to_dna import rna_to_dna



# Future imports
# from .analysis.gc_content import gc_content
# from .analysis.complement import complement


def run_selected_analysis(sequence, sequence_type, selected_tools):

    results = {}

    analysis_map = {

    "dna_to_rna": (
        "DNA → RNA",
        dna_to_rna
    ),

    "rna_to_dna": (
        "RNA → DNA",
        rna_to_dna
    ),

}

    for tool in selected_tools:

        if tool in analysis_map:

            title, function = analysis_map[tool]

            results[title] = function(sequence)

    return results