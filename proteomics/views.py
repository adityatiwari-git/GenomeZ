import re
from collections import Counter
from pathlib import Path
from urllib.parse import quote

import requests
from django.conf import settings
from django.shortcuts import render


VALID_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")

AVERAGE_MASS = {
    "A": 89.09, "R": 174.20, "N": 132.12, "D": 133.10,
    "C": 121.15, "E": 147.13, "Q": 146.15, "G": 75.07,
    "H": 155.16, "I": 131.17, "L": 131.17, "K": 146.19,
    "M": 149.21, "F": 165.19, "P": 115.13, "S": 105.09,
    "T": 119.12, "W": 204.23, "Y": 181.19, "V": 117.15,
}

HYDROPHOBIC = set("AILMFWVYV")


def clean_sequence(text):
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(">"):
            continue
        lines.append(line)
    return re.sub(r"[^A-Za-z]", "", "".join(lines)).upper()


def validate_protein(sequence):
    if not sequence:
        return {"valid": False, "message": "Protein sequence is empty."}

    invalid = sorted(set(sequence) - VALID_AMINO_ACIDS)
    if invalid:
        return {
            "valid": False,
            "message": "Invalid amino-acid sequence.",
            "invalid": invalid,
        }

    return {"valid": True, "sequence": sequence, "length": len(sequence)}


def analyze_protein(sequence):
    counts = Counter(sequence)
    length = len(sequence)
    molecular_weight = sum(AVERAGE_MASS[aa] for aa in sequence) - (length - 1) * 18.015
    hydrophobic_count = sum(aa in HYDROPHOBIC for aa in sequence)

    return {
        "length": length,
        "molecular_weight": round(molecular_weight, 2),
        "hydrophobic_percent": round((hydrophobic_count / length) * 100, 2),
        "composition": {aa: counts.get(aa, 0) for aa in sorted(VALID_AMINO_ACIDS)},
    }


def uniprot_search(sequence):
    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": f"\"{sequence}\"",
        "format": "tsv",
        "fields": "accession,id,protein_name,gene_names,organism_name,length",
        "size": 5,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15,
            headers={"User-Agent": "GenomeZ/1.0"},
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        return {"error": f"UniProt search failed: {exc}"}

    lines = [line for line in response.text.splitlines() if line.strip()]
    if len(lines) < 2:
        return {"matches": []}

    headers = lines[0].split("\t")
    matches = []

    for line in lines[1:]:
        values = line.split("\t")
        row = dict(zip(headers, values))
        accession = row.get("Entry", "")

        matches.append({
            "accession": accession,
            "id": row.get("Entry Name", ""),
            "protein_name": row.get("Protein names", ""),
            "gene": row.get("Gene Names", ""),
            "organism": row.get("Organism", ""),
            "length": row.get("Length", ""),
            "url": f"https://www.uniprot.org/uniprotkb/{accession}" if accession else "",
        })

    return {"matches": matches}


def build_blast_url(sequence):
    return (
        "https://blast.ncbi.nlm.nih.gov/Blast.cgi?"
        "PROGRAM=blastp&PAGE_TYPE=BlastSearch&QUERY=" + quote(sequence)
    )


def load_sample_sequence():
    path = Path(settings.BASE_DIR) / "sample_protein.fasta"
    if not path.exists():
        return ""

    return clean_sequence(path.read_text(encoding="utf-8"))


def proteomics_home(request):
    context = {"sequence": ""}

    if request.method == "POST":
        action = request.POST.get("action", "analyze")

        if action == "load_sample":
            context["sequence"] = load_sample_sequence()
            return render(request, "proteomics/proteomics.html", context)

        sequence = request.POST.get("sequence", "")
        uploaded = request.FILES.get("sequence_file")

        if uploaded:
            try:
                sequence = uploaded.read().decode("utf-8")
            except UnicodeDecodeError:
                context["error"] = "The uploaded file could not be read as text."
                return render(request, "proteomics/proteomics.html", context)

        sequence = clean_sequence(sequence)
        context["sequence"] = sequence
        validation = validate_protein(sequence)
        context["validation"] = validation

        if validation["valid"]:
            context["analysis"] = analyze_protein(sequence)
            context["blast_url"] = build_blast_url(sequence)
            context["search"] = uniprot_search(sequence)

            if action == "analyze":
                request.session["last_protein"] = sequence

    elif request.session.get("last_protein"):
        context["sequence"] = request.session["last_protein"]

    return render(request, "proteomics/proteomics.html", context)
