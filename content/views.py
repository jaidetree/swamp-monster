"""Views for the `content` app: the public Works listing and gallery pages."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Work


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
