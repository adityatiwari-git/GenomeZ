from datetime import datetime


def generate_txt_report(sequence, sequence_type, results):
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

    for title, value in results.items():
        report.extend([
            "",
            title,
            "-" * len(title),
            value["display"],
        ])

    return "\n".join(report)
