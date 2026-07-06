from django.shortcuts import render

def analyzer_home(request):
    return render(request, "analyzer/analyzer.html")