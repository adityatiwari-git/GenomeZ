from django.urls import path
from . import views

urlpatterns = [
    path("", views.analyzer_home, name="analyzer"),

    path("download-report/",
        views.download_report,
        name="download_report"),
    
    path(
        "download/fasta/<str:analysis>/",
        views.download_fasta,
        name="download_fasta",),
    
    
]

    