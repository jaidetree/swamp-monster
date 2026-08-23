"""Views for the `swamp` app: the Home page, the public Works listing and
gallery pages, and the contact form."""

import logging

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import ContactForm
from .models import ContactSubmission, Resource, Training, Work

logger = logging.getLogger(__name__)

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
        "swamp/home.html",
        {"works": works, "trainings": trainings, "resources": resources},
    )


def work_list(request: HttpRequest) -> HttpResponse:
    """The full portfolio listing: every published Work, owner-controlled order.

    Unlike the (future) Home page teaser, this applies no ``featured`` filter.
    """
    works = Work.objects.filter(published=True).order_by("order")
    return render(request, "swamp/work_list.html", {"works": works})


def work_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """A single Work's full image gallery, images in ``order`` with captions."""
    work = get_object_or_404(Work, slug=slug, published=True)
    images = work.images.order_by("order")
    return render(request, "swamp/work_detail.html", {"work": work, "images": images})


def contact(request: HttpRequest) -> HttpResponse:
    """The public contact form.

    A valid POST persists a `ContactSubmission` row first, then attempts the
    Postmark notification email. The email send is best-effort: a failure is
    logged, never raised past this view, so it can't roll back or block the
    already-committed DB record (ticket 15's core acceptance criterion).
    """
    success = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = ContactSubmission.objects.create(**form.cleaned_data)
            _send_contact_notification(submission)
            success = True
            form = ContactForm()
    else:
        form = ContactForm()
    return render(request, "swamp/contact.html", {"form": form, "success": success})


def _send_contact_notification(submission: ContactSubmission) -> None:
    """Best-effort notification email for a just-saved submission.

    Any send failure (bad credentials, Postmark outage, ...) is logged and
    swallowed rather than propagated — the DB row is already committed and
    must stand regardless of email delivery.
    """
    try:
        send_mail(
            subject=f"New contact form submission from {submission.name}",
            message=submission.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
        )
    except Exception:
        logger.exception(
            "Failed to send contact notification email for submission %s", submission.pk
        )
