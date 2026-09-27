from django.urls import path
from . import views

urlpatterns = [
    path("", views.proteomics_home, name="proteomics"),
]
