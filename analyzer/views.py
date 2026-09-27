from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .validators import validate_sequence
from .services import run_selected_analysis

from django.http import HttpResponse
from .report_generator import generate_txt_report
from .fasta_generator import generate_fasta

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

PREMIUM_TOOLS = {
    "blast",
}

@login_required
def analyzer_home(request):

    context = {
    "result": None,
    "uploaded_sequence": ""
}

    if request.method == "POST":

        uploaded = request.FILES.get("sequence_file") or request.FILES.get("fasta_file") or request.FILES.get("txt_file")
        if uploaded:
            from .analysis.file_parser import parse_uploaded_file
            sequence = parse_uploaded_file(uploaded)
        else:
            sequence = request.POST.get("sequence", "")

# ADD THIS LINE
        context["uploaded_sequence"] = sequence
        result = validate_sequence(sequence)
        context["result"] = result
        
        if result["valid"]:

            selected_tools = request.POST.getlist("analysis")

            allowed_tools = FREE_TOOLS | PREMIUM_TOOLS
            selected_tools = [tool for tool in selected_tools if tool in allowed_tools]

            if "blast" in selected_tools and not request.user.is_authenticated:
                selected_tools.remove("blast")
            motif = request.POST.get("motif", "").strip()
            
            context["analysis_results"] = run_selected_analysis(
                result["sequence"],
                result["type"],
                selected_tools, 
                motif)
            
            from .download_utils import SEQUENCE_ANALYSES

            context["sequence_analyses"] = SEQUENCE_ANALYSES

            request.session["sequence"] = result["sequence"]
            request.session["sequence_type"] = result["type"]
            request.session["results"] = context["analysis_results"]
            
            context["premium_tools"] = PREMIUM_TOOLS
        context["is_authenticated"] = request.user.is_authenticated

    return render(
        request,
        "analyzer/analyzer.html",
        context
    )
    
    
def download_report(request):

    sequence = request.session.get("sequence")
    sequence_type = request.session.get("sequence_type")
    results = request.session.get("results")

    report = generate_txt_report(
        sequence,
        sequence_type,
        results
    )

    response = HttpResponse(
        report,
        content_type="text/plain"
    )

    response["Content-Disposition"] = (
        'attachment; filename="GenomeZ_Report.txt"'
    )

    return response


def download_fasta(request, analysis):

    results = request.session.get("results", {})

    if analysis not in results:
        return HttpResponse("Result not found.", status=404)

    result = results[analysis]

    if result.get("format") != "sequence":
        return HttpResponse(
            "This analysis cannot be exported as FASTA.",
            status=400
        )

    fasta = generate_fasta(
        analysis.replace(" ", "_"),
        result["raw"]
    )

    response = HttpResponse(
        fasta,
        content_type="text/plain"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{analysis.replace(" ", "_")}.fasta"'
    )

    return response