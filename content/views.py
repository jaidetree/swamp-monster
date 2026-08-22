"""Views for the `content` app: the Home page and the public Works listing
and gallery pages."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Resource, Training, Work

#: Sane caps on the Home page teasers — enough to show a showcase without the
#: page growing unbounded as the owner adds more published/featured rows.
WORKS_TEASER_LIMIT = 6
TRAINING_TEASER_LIMIT = 3
RESOURCE_TEASER_LIMIT = 3


def home(request: HttpRequest) -> HttpResponse:
    """The Home page: a static hero plus featured Works/Training/Resource
    teasers.

    Each teaser applies the same `published=True, featured=True` filter,
    ordered by `order`; the template renders each section gracefully (no
    CMS-editor-facing placeholder text) when a section has zero qualifying
    rows, which is the common case before the owner has featured anything.
    """
    works = Work.objects.filter(published=True, featured=True).order_by("order")[
        :WORKS_TEASER_LIMIT
    ]
    trainings = Training.objects.filter(published=True, featured=True).order_by("order")[
        :TRAINING_TEASER_LIMIT
    ]
    resources = Resource.objects.filter(published=True, featured=True).order_by("order")[
        :RESOURCE_TEASER_LIMIT
    ]
    return render(
        request,
        "content/home.html",
        {"works": works, "trainings": trainings, "resources": resources},
    )


def work_list(request: HttpRequest) -> HttpResponse:
    """The full portfolio listing: every published Work, owner-controlled order.

    Unlike the (future) Home page teaser, this applies no ``featured`` filter.
    """
    works = Work.objects.filter(published=True).order_by("order")
    return render(request, "content/work_list.html", {"works": works})


def work_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """A single Work's full image gallery, images in ``order`` with captions."""
    work = get_object_or_404(Work, slug=slug, published=True)
    images = work.images.order_by("order")
    return render(request, "content/work_detail.html", {"work": work, "images": images})
