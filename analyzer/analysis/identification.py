import re

import requests


def identify_sequence(sequence):
    """Submit a DNA sequence to NCBI BLASTN and return its request ID."""
    url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
    data = {
        "CMD": "Put",
        "PROGRAM": "blastn",
        "DATABASE": "nt",
        "QUERY": sequence,
        "FORMAT_TYPE": "XML",
    }

    try:
        response = requests.post(
            url,
            data=data,
            timeout=20,
            headers={"User-Agent": "GenomeZ/1.0"},
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        return {"error": str(exc), "rid": None, "message": ""}

    match = re.search(r"RID = ([A-Z0-9-]+)", response.text)
    if not match:
        return {
            "error": "NCBI did not return a request ID.",
            "rid": None,
            "message": "",
        }

    rid = match.group(1)
    return {
        "error": None,
        "rid": rid,
        "message": f"BLASTN request submitted (RID: {rid}).",
    }
