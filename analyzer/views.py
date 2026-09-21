from django.shortcuts import render
from urllib.parse import quote

from .validators import validate_sequence
from .services import run_selected_analysis

from django.http import HttpResponse
from .report_generator import generate_txt_report
from .fasta_generator import generate_fasta

def analyzer_home(request):

    context = {
    "result": None,
    "uploaded_sequence": ""
}

    if request.method == "POST":

        uploaded = request.FILES.get("fasta_file") or request.FILES.get("txt_file")
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
            
    return render(
        request,
        "analyzer/analyzer.html",
        context
    )
    
    
def download_report(request):

    sequence = request.session.get("sequence")
    sequence_type = request.session.get("sequence_type")
    results = request.session.get("results", {})

    if not sequence or not sequence_type or not results:
        return HttpResponse("No analysis results available.", status=400)

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