from django.urls import path
from . import views

urlpatterns = [
    path("", views.analyzer_home, name="analyzer"),
]