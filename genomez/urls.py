from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("analyzer/", include("analyzer.urls")),
    path("proteomics/", include("proteomics.urls")),
]
