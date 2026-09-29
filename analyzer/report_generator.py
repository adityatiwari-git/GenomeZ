from datetime import datetime


def generate_txt_report(sequence, sequence_type, results):
    """Build a simple text report from the latest GenomeZ analysis."""
    report = [
        "=" * 50,
        "GenomeZ Analysis Report",
        "=" * 50,
        "",
        f"Generated : {datetime.now()}",
        f"Sequence Type : {sequence_type}",
        f"Sequence Length : {len(sequence)} bp",
        "",
        "Sequence",
        "-" * 50,
        sequence,
        "",
        "Analysis Results",
        "-" * 50,
    ]

    for title, result in results.items():
        report.extend([
            "",
            title,
            "-" * len(title),
            result["display"],
        ])

    return "\n".join(report)
