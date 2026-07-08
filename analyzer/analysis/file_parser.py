"""
GenomeZ
File Parser
"""


def parse_uploaded_file(uploaded_file):

    content = uploaded_file.read().decode("utf-8")

    if uploaded_file.name.endswith((".fasta", ".fa")):

        lines = content.splitlines()

        sequence = "".join(
            line.strip()
            for line in lines
            if not line.startswith(">")
        )

        return sequence

    return content.strip()