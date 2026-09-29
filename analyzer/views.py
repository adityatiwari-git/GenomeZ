from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .analysis.file_parser import parse_uploaded_file
from .download_utils import SEQUENCE_ANALYSES
from .fasta_generator import generate_fasta
from .report_generator import generate_txt_report
from .services import run_selected_analysis
from .validators import validate_sequence


FREE_TOOLS = {
    "dna_to_rna",
    "rna_to_dna",
    "gc_content",
    "atgc_count",
    "complement",
    "reverse_complement",
    "translation",
    "motif",
    "orf",
}

PREMIUM_TOOLS = {"blast"}

SAMPLE_FILES = {
    "dna": "sample.fasta",
    "rna": "sample_rna.fasta",
}


def load_sample_sequence(sample_key):
    """Load one of the sample DNA/RNA files from the project root."""
    filename = SAMPLE_FILES.get(sample_key)

    if not filename:
        return ""

    sample_path = Path(settings.BASE_DIR) / filename

    if not sample_path.exists():
        return ""

    content = sample_path.read_text(encoding="utf-8")
    sequence = []

    for line in content.splitlines():
        line = line.strip()
        if line and not line.startswith(">"):
            sequence.append(line)

    return "".join(sequence)


def get_sequence_from_request(request):
    """Get a sequence from a sample, uploaded file, or text box."""
    sample_key = request.POST.get("sample_sequence", "")

    if sample_key:
        return load_sample_sequence(sample_key)

    uploaded_file = (
        request.FILES.get("sequence_file")
        or request.FILES.get("fasta_file")
        or request.FILES.get("txt_file")
    )

    if uploaded_file:
        return parse_uploaded_file(uploaded_file)

    return request.POST.get("sequence", "")


def analyzer_home(request):
    context = {
        "result": None,
        "uploaded_sequence": "",
        "is_authenticated": request.user.is_authenticated,
    }

    if request.method == "POST":
        sequence = get_sequence_from_request(request)
        action = request.POST.get("action", "analyze")
        context["uploaded_sequence"] = sequence

        # Loading a sample only fills the sequence box. It does not run analysis.
        if action == "load_sample":
            return render(request, "analyzer/analyzer.html", context)

        validation = validate_sequence(sequence)
        context["result"] = validation

        if validation["valid"]:
            selected_tools = request.POST.getlist("analysis")
            allowed_tools = FREE_TOOLS | PREMIUM_TOOLS
            selected_tools = [
                tool for tool in selected_tools
                if tool in allowed_tools
            ]

            # BLAST is the only premium analyzer tool at the moment.
            if "blast" in selected_tools and not request.user.is_authenticated:
                login_url = reverse("login")
                analyzer_url = reverse("analyzer")
                return redirect(f"{login_url}?next={analyzer_url}")

            motif = request.POST.get("motif", "").strip()

            analysis_results = run_selected_analysis(
                validation["sequence"],
                validation["type"],
                selected_tools,
                motif,
            )

            context["analysis_results"] = analysis_results
            context["sequence_analyses"] = SEQUENCE_ANALYSES
            context["premium_tools"] = PREMIUM_TOOLS

            # Keep the latest analysis in the session for the download views.
            request.session["sequence"] = validation["sequence"]
            request.session["sequence_type"] = validation["type"]
            request.session["results"] = analysis_results

    return render(request, "analyzer/analyzer.html", context)


def download_report(request):
    """Download the latest analysis results as a text report."""
    sequence = request.session.get("sequence")
    sequence_type = request.session.get("sequence_type")
    results = request.session.get("results")

    report = generate_txt_report(sequence, sequence_type, results)
    response = HttpResponse(report, content_type="text/plain")
    response["Content-Disposition"] = 'attachment; filename="GenomeZ_Report.txt"'
    return response


def download_fasta(request, analysis):
    """Download a sequence-type analysis result as a FASTA file."""
    results = request.session.get("results", {})

    if analysis not in results:
        return HttpResponse("Result not found.", status=404)

    result = results[analysis]

    if result.get("format") != "sequence":
        return HttpResponse(
            "This analysis cannot be exported as FASTA.",
            status=400,
        )

    filename = analysis.replace(" ", "_")
    fasta = generate_fasta(filename, result["raw"])

    response = HttpResponse(fasta, content_type="text/plain")
    response["Content-Disposition"] = f'attachment; filename="{filename}.fasta"'
    return response
