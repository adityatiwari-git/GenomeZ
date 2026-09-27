from django.shortcuts import render


def proteomics_home(request):
    return render(request, "proteomics/proteomics.html")
