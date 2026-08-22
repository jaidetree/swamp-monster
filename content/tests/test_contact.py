"""Tests for the `/contact` page and Postmark notification (ticket 15).

All email assertions run against Anymail's test/dummy backend
(`anymail.backends.test.EmailBackend`), which records sends in
`django.core.mail.outbox` without touching the network — no real Postmark
credentials are needed, or used, here.
"""

from unittest.mock import patch

import pytest
from django.core import mail
from django.test import override_settings
from django.urls import reverse

from content.models import ContactSubmission

TEST_EMAIL_BACKEND = "anymail.backends.test.EmailBackend"


@pytest.mark.django_db
def test_contact_get_renders_form(client):
    response = client.get(reverse("contact"))

    assert response.status_code == 200
    assert b'name="name"' in response.content
    assert b'name="email"' in response.content
    assert b'name="message"' in response.content


@pytest.mark.django_db
def test_contact_post_invalid_shows_errors_and_does_not_persist(client):
    response = client.post(
        reverse("contact"),
        {"name": "", "email": "not-an-email", "message": ""},
    )

    assert response.status_code == 200
    assert response.context["form"].errors
    assert ContactSubmission.objects.count() == 0


@pytest.mark.django_db
@override_settings(EMAIL_BACKEND=TEST_EMAIL_BACKEND)
def test_contact_post_valid_creates_submission_and_sends_email(client):
    response = client.post(
        reverse("contact"),
        {
            "name": "Jamie Visitor",
            "email": "jamie@example.com",
            "message": "Interested in a custom bag.",
        },
    )

    assert response.status_code == 200
    assert response.context["success"] is True

    submission = ContactSubmission.objects.get()
    assert submission.name == "Jamie Visitor"
    assert submission.email == "jamie@example.com"
    assert submission.message == "Interested in a custom bag."

    assert len(mail.outbox) == 1
    sent = mail.outbox[0]
    assert "Jamie Visitor" in sent.subject
    assert sent.to == ["hello@swamp-monster-leather.com"]


@pytest.mark.django_db
@override_settings(EMAIL_BACKEND=TEST_EMAIL_BACKEND)
def test_contact_post_valid_resets_form_on_success(client):
    response = client.post(
        reverse("contact"),
        {
            "name": "Jamie Visitor",
            "email": "jamie@example.com",
            "message": "Interested in a custom bag.",
        },
    )

    assert response.context["form"].data == {}


@pytest.mark.django_db
@override_settings(EMAIL_BACKEND=TEST_EMAIL_BACKEND)
def test_contact_post_email_failure_still_persists_submission(client):
    with patch("content.views.send_mail", side_effect=RuntimeError("Postmark is down")):
        response = client.post(
            reverse("contact"),
            {
                "name": "Jamie Visitor",
                "email": "jamie@example.com",
                "message": "Interested in a custom bag.",
            },
        )

    assert response.status_code == 200
    assert response.context["success"] is True
    submission = ContactSubmission.objects.get()
    assert submission.name == "Jamie Visitor"
    assert len(mail.outbox) == 0
