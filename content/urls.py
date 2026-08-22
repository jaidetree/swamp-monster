"""URL patterns for the `content` app, included under `/works` by swamp.urls."""

from django.urls import path

from . import views

app_name = "content"

urlpatterns = [
    path("", views.work_list, name="work_list"),
    path("<slug:slug>/", views.work_detail, name="work_detail"),
]
