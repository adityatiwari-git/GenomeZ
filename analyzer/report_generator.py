from datetime import datetime


def generate_txt_report(sequence, sequence_type, results):

    report = []

    report.append("=" * 50)
    report.append("GenomeZ Analysis Report")
    report.append("=" * 50)
    report.append("")

    report.append(f"Generated : {datetime.now()}")
    report.append(f"Sequence Type : {sequence_type}")
    report.append(f"Sequence Length : {len(sequence)} bp")

    report.append("")
    report.append("Sequence")
    report.append("-" * 50)
    report.append(sequence)

    report.append("")
    report.append("Analysis Results")
    report.append("-" * 50)

    for title, value in results.items():

        report.append("")
        report.append(title)
        report.append("-" * len(title))

        report.append(value["display"])


