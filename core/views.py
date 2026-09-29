from django.shortcuts import render


def home(request):
    """Show the public GenomeZ homepage."""
    return render(request, "base/home.html")
