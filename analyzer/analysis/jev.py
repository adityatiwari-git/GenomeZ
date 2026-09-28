import os

import requests


JEVMODEL_ENDPOINT = "https://jevmodel.org/v1/systemone"


def get_recommendation(sequence, sequence_type, analysis_results):
    api_key = os.environ.get("JEVMODEL_API_KEY")

    if not api_key:
        return {
            "available": False,
            "message": "Smart Recommendation is unavailable because the Jev API key is not configured.",
        }

    state = (
        f"Sequence type: {sequence_type}\n"
        f"Sequence length: {len(sequence)}\n"
        f"Sequence: {sequence[:4000]}\n"
        f"Existing analysis results: {analysis_results}"
    )

    payload = {
        "model": "jev-latest",
        "state": state,
        "questions": {
            "next_action": {
                "type": "choice",
                "instructions": "Which next analysis would be most useful for this sequence?",
                "criteria": {
                    "orf": "Look for open reading frames and coding regions.",
                    "motif": "Search for sequence motifs or repeated patterns.",
                    "composition": "Inspect nucleotide composition and GC/base distribution.",
                    "identification": "Use database-based sequence identification.",
                    "general": "Continue with a broad set of standard sequence analyses.",
                },
            },
            "database_search": {
                "type": "noul",
                "instructions": "Would an external database search such as NCBI BLAST be useful for this sequence?",
            },
        },
    }

    try:
        response = requests.post(
            JEVMODEL_ENDPOINT,
            json=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        return {
            "available": False,
            "message": f"Jev request failed: {exc}",
        }
    except ValueError:
        return {
            "available": False,
            "message": "Jev returned an invalid response.",
        }

    questions = data.get("questions", {})
    next_action = questions.get("next_action", {})
    database_search = questions.get("database_search", {})

    return {
        "available": True,
        "next_action": next_action.get("value") or next_action.get("choice"),
        "next_action_probability": next_action.get("probabilities"),
        "database_search": database_search.get("value"),
        "database_probability": database_search.get("probability"),
        "raw": data,
    }
