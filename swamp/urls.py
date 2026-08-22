"""URL configuration for the swamp project."""

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import path


def health(request: HttpRequest) -> HttpResponse:
    """Empty-app smoke-test root: proves the app boots and responds."""
    return HttpResponse("ok")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", health, name="health"),
]
