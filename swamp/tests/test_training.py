"""Tests for the `/training` landing page and its training-request form.

Mirrors `test_contact.py`'s structure, but persists a `Training` row (its
subject is implicitly "Training") rather than `ContactSubmission`. The
Mailjet notification is best-effort, verified against Anymail's test backend
rather than a real network call.
"""

from unittest.mock import patch

import pytest
from django.core import mail
from django.test import override_settings
from django.urls import reverse

from swamp.models import Training

TEST_EMAIL_BACKEND = "anymail.backends.test.EmailBackend"


@pytest.mark.django_db
def test_training_get_renders_landing_content_and_form(client):
    response = client.get(reverse("training"))

    assert response.status_code == 200
    assert b"Possible Projects" in response.content
    assert b"How It Works" in response.content
    assert b'name="name"' in response.content
    assert b'name="email"' in response.content
    assert b'name="target_dates"' in response.content
    assert b'name="message"' in response.content
    assert b'name="subject"' not in response.content


@pytest.mark.django_db
def test_training_post_missing_dates_shows_error_and_does_not_persist(client):
    response = client.post(
        reverse("training"),
        {
            "name": "Jamie Visitor",
            "email": "jamie@example.com",
            "message": "I'd like to make a wallet.",
        },
    )

    assert response.status_code == 200
    assert "target_dates" in response.context["form"].errors
    assert Training.objects.count() == 0


@pytest.mark.django_db
def test_training_post_invalid_date_shows_error_and_does_not_persist(client):
    response = client.post(
        reverse("training"),
        {
            "name": "Jamie Visitor",
            "email": "jamie@example.com",
            "target_dates": ["not-a-date"],
            "message": "I'd like to make a wallet.",
        },
    )

    assert response.status_code == 200
    assert "target_dates" in response.context["form"].errors
    assert Training.objects.count() == 0


@pytest.mark.django_db
@override_settings(EMAIL_BACKEND=TEST_EMAIL_BACKEND)
def test_training_post_valid_single_date_creates_submission_and_sends_email(client):
    response = client.post(
        reverse("training"),
        {
            "name": "Jamie Visitor",
            "email": "jamie@example.com",
            "target_dates": ["2026-10-01"],
            "message": "I'd like to make a wallet.",
        },
    )

    assert response.status_code == 200
    assert response.context["success"] is True

    submission = Training.objects.get()
    assert submission.name == "Jamie Visitor"
    assert submission.email == "jamie@example.com"
    assert submission.message == "I'd like to make a wallet."
    assert [d.isoformat() for d in submission.target_dates] == ["2026-10-01"]

    assert len(mail.outbox) == 1
    sent = mail.outbox[0]
    assert sent.subject == "Training"
    assert sent.to == ["info+form@swampmonsterleather.com"]
    assert sent.reply_to == ["jamie@example.com"]
    assert "2026-10-01" in sent.body


@pytest.mark.django_db
@override_settings(EMAIL_BACKEND=TEST_EMAIL_BACKEND)
def test_training_post_valid_multiple_dates_stores_all_dates(client):
    response = client.post(
        reverse("training"),
        {
            "name": "Jamie Visitor",
            "email": "jamie@example.com",
            "target_dates": ["2026-10-01", "2026-10-15"],
            "message": "I'd like to make a wallet.",
        },
    )

    assert response.status_code == 200
    submission = Training.objects.get()
    assert [d.isoformat() for d in submission.target_dates] == ["2026-10-01", "2026-10-15"]


@pytest.mark.django_db
@override_settings(EMAIL_BACKEND=TEST_EMAIL_BACKEND)
def test_training_post_valid_resets_form_on_success(client):
    response = client.post(
        reverse("training"),
        {
            "name": "Jamie Visitor",
            "email": "jamie@example.com",
            "target_dates": ["2026-10-01"],
            "message": "I'd like to make a wallet.",
        },
    )

    assert response.context["form"].data == {}


@pytest.mark.django_db
@override_settings(EMAIL_BACKEND=TEST_EMAIL_BACKEND)
def test_training_post_email_failure_still_persists_submission(client):
    with patch("swamp.views.EmailMessage.send", side_effect=RuntimeError("Postmark is down")):
        response = client.post(
            reverse("training"),
            {
                "name": "Jamie Visitor",
                "email": "jamie@example.com",
                "target_dates": ["2026-10-01"],
                "message": "I'd like to make a wallet.",
            },
        )

    assert response.status_code == 200
    assert response.context["success"] is True
    submission = Training.objects.get()
    assert submission.name == "Jamie Visitor"
    assert len(mail.outbox) == 0
