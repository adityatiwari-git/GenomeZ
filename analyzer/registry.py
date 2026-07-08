from .analysis.dna_to_rna import dna_to_rna
from .analysis.rna_to_dna import rna_to_dna
from .analysis.complement import complement
from .analysis.reverse_complement import reverse_complement
from .analysis.gc_content import gc_content
from .analysis.atgc_count import atgc_count
from .analysis.translation import translate

ANALYSIS_REGISTRY = {
    "dna_to_rna": dna_to_rna,
    "rna_to_dna": rna_to_dna,
    "complement": complement,
    "reverse_complement": reverse_complement,
    "gc_content": gc_content,
    "atgc_count": atgc_count,
    "translation": translate,
}