from django.shortcuts import render


def home(request):
    """Show the public GenomeZ homepage."""
    return render(request, "base/home.html")


def documentation(request):
    """Show the GenomeZ documentation."""
    return render(request, "base/documentation.html")
