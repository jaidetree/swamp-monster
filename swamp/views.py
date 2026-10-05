"""Views for the `swamp` app: the Home page, the public Works listing, and
the contact form."""

import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import ContactForm, TrainingRequestForm
from .models import ContactSubmission, Resource, Training, Work

logger = logging.getLogger(__name__)

#: Sane caps on the Home page teasers — enough to show a showcase without the
#: page growing unbounded as the owner adds more published/featured rows.
WORKS_TEASER_LIMIT = 6
RESOURCE_TEASER_LIMIT = 3


def home(request: HttpRequest) -> HttpResponse:
    """The Home page: a static hero plus featured Works/Resource teasers.

    Each teaser applies the same `published=True, featured=True` filter,
    ordered by `order`; the template renders each section gracefully (no
    CMS-editor-facing placeholder text) when a section has zero qualifying
    rows, which is the common case before the owner has featured anything.
    """
    works = Work.objects.filter(published=True, featured=True).order_by("order")[
        :WORKS_TEASER_LIMIT
    ]
    resources = Resource.objects.filter(published=True, featured=True).order_by("order")[
        :RESOURCE_TEASER_LIMIT
    ]
    return render(
        request,
        "swamp/home.html",
        {"works": works, "resources": resources},
    )


def work_list(request: HttpRequest) -> HttpResponse:
    """The full portfolio listing: every published Work, newest first.

    Unlike the Home page teaser (owner-curated via ``featured``/``order``),
    this applies no ``featured`` filter and orders by ``created_at`` so newly
    published pieces surface automatically without owner upkeep.
    """
    works = Work.objects.filter(published=True).order_by("-created_at")
    return render(request, "swamp/work_list.html", {"works": works})


def contact(request: HttpRequest) -> HttpResponse:
    """The public contact form.

    A valid POST persists a `ContactSubmission` row first, then attempts the
    Mailjet notification email. The email send is best-effort: a failure is
    logged, never raised past this view, so it can't roll back or block the
    already-committed DB record (ticket 15's core acceptance criterion).
    """
    success = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = ContactSubmission.objects.create(**form.cleaned_data)
            _send_notification(
                subject=submission.subject,
                body=submission.message,
                reply_to=submission.email,
                log_ref=f"contact submission {submission.pk}",
            )
            success = True
            form = ContactForm()
    else:
        form = ContactForm()
    return render(request, "swamp/contact.html", {"form": form, "success": success})


def training(request: HttpRequest) -> HttpResponse:
    """The Training landing page and its training-request form.

    The form is `ContactForm`'s shape plus `target_dates`; a valid POST
    persists a `Training` row (rather than `ContactSubmission` — its subject
    is implicitly "Training") and notifies exactly like `contact()`.
    """
    success = False
    if request.method == "POST":
        form = TrainingRequestForm(request.POST)
        if form.is_valid():
            submission = Training.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                message=form.cleaned_data["message"],
                target_dates=form.cleaned_data["target_dates"],
            )
            _send_notification(
                subject="Training",
                body=_training_email_body(submission),
                reply_to=submission.email,
                log_ref=f"training request {submission.pk}",
            )
            success = True
            form = TrainingRequestForm()
    else:
        form = TrainingRequestForm()
    return render(request, "swamp/training.html", {"form": form, "success": success})


def _training_email_body(submission: Training) -> str:
    """The training-request notification body: the visitor's message with
    their proposed dates appended, since those live in a separate column."""
    dates = ", ".join(date.isoformat() for date in submission.target_dates)
    return f"{submission.message}\n\nRequested dates: {dates}"


def _send_notification(*, subject: str, body: str, reply_to: str, log_ref: str) -> None:
    """Best-effort notification email shared by `contact()` and `training()`.

    Any send failure (bad credentials, Mailjet outage, ...) is logged and
    swallowed rather than propagated — the DB row is already committed and
    must stand regardless of email delivery.
    """
    try:
        EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_NOTIFICATION_EMAIL],
            reply_to=[reply_to],
        ).send()
    except Exception:
        logger.exception("Failed to send notification email for %s", log_ref)
