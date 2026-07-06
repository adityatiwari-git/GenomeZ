from django.shortcuts import render
from .validators import validate_dna


def analyzer_home(request):
    context = {}

    if request.method == "POST":
        sequence = request.POST.get("sequence", "")
        context["result"] = validate_dna(sequence)

    return render(request, "analyzer/analyzer.html", context)