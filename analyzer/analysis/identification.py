import re
import time

import requests


BLAST_URL = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
HEADERS = {"User-Agent": "GenomeZ/1.0"}


def identify_sequence(sequence):
    """Send a DNA sequence to NCBI BLASTN and return up to five matches."""
    try:
        response = requests.post(
            BLAST_URL,
            data={
                "CMD": "Put",
                "PROGRAM": "blastn",
                "DATABASE": "nt",
                "QUERY": sequence,
                "FORMAT_TYPE": "XML",
            },
            timeout=20,
            headers=HEADERS,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        return {"error": str(error), "rid": None, "hits": [], "message": ""}

    request_id = re.search(r"RID = ([A-Z0-9-]+)", response.text)

    if not request_id:
        return {
            "error": "NCBI did not return a request ID.",
            "rid": None,
            "hits": [],
            "message": "",
        }

    rid = request_id.group(1)

    for _ in range(3):
        time.sleep(2)

        try:
            result = requests.get(
                BLAST_URL,
                params={
                    "CMD": "Get",
                    "RID": rid,
                    "FORMAT_TYPE": "XML",
                },
                timeout=20,
                headers=HEADERS,
            )
            result.raise_for_status()
        except requests.RequestException as error:
            return {"error": str(error), "rid": rid, "hits": [], "message": ""}

        xml = result.text

        if "Status=WAITING" in xml:
            continue

        hits = []

        for block in re.findall(r"<Hit>(.*?)</Hit>", xml, re.DOTALL)[:5]:
            accession = re.search(r"<Hit_accession>(.*?)</Hit_accession>", block)
            title = re.search(r"<Hit_def>(.*?)</Hit_def>", block)
            identity = re.search(r"<Hsp_identity>(.*?)</Hsp_identity>", block)
            alignment_length = re.search(
                r"<Hsp_align-len>(.*?)</Hsp_align-len>", block
            )
            evalue = re.search(r"<Hsp_evalue>(.*?)</Hsp_evalue>", block)

            identity_percent = ""
            if identity and alignment_length:
                length = int(alignment_length.group(1))
                if length:
                    identity_percent = round(
                        int(identity.group(1)) / length * 100,
                        2,
                    )

            hits.append({
                "accession": accession.group(1) if accession else "",
                "title": title.group(1) if title else "",
                "identity": identity_percent,
                "evalue": evalue.group(1) if evalue else "",
            })

        return {
            "error": None,
            "rid": rid,
            "hits": hits,
            "message": f"Found {len(hits)} NCBI BLASTN match(es).",
        }

    return {
        "error": None,
        "rid": rid,
        "hits": [],
        "message": f"BLASTN is still processing (RID: {rid}).",
    }
