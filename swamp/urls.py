"""URL configuration for the swamp project."""

from django.conf import settings
from django.conf.urls.static import static
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

if settings.DEBUG:
    # Dev-only: serve MEDIA_ROOT directly (WhiteNoise only covers STATIC_ROOT).
    # Production media storage is Cloudflare R2 (ticket 16), which won't need this.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
