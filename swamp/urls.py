"""URL configuration for the swamp project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from content import views as content_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("works/", include("content.urls")),
    path("contact/", content_views.contact, name="contact"),
    path("", content_views.home, name="home"),
]

if settings.DEBUG:
    # Dev-only: serve MEDIA_ROOT directly (WhiteNoise only covers STATIC_ROOT).
    # Production media storage is Cloudflare R2 (ticket 16), which won't need this.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
