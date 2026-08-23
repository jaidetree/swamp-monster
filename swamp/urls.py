"""URL patterns for the `swamp` app, included under `/works` by config.urls."""

from django.urls import path

from . import views

app_name = "swamp"

urlpatterns = [
    path("", views.work_list, name="work_list"),
    path("<slug:slug>/", views.work_detail, name="work_detail"),
]
