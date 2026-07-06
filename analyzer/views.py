from django.shortcuts import render

from .validators import validate_sequence
from .services import run_selected_analysis


def analyzer_home(request):

    context = {}

    if request.method == "POST":

        sequence = request.POST.get("sequence", "")

        result = validate_sequence(sequence)

        context["result"] = result

        if result["valid"]:

            selected_tools = request.POST.getlist("analysis")

            context["analysis_results"] = run_selected_analysis(
    result["sequence"],
    result["type"],
    selected_tools
)

    return render(
        request,
        "analyzer/analyzer.html",
        context
    )