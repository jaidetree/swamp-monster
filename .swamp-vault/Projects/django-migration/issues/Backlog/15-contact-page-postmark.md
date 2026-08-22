---
tags:
    - ready-for-agent
type: task
blocked_by:
    - "[[/Projects/django-migration/issues/Backlog/12-training-resource-contactsubmission-models|12-training-resource-contactsubmission-models]]"
---

# Contact Page & Postmark Integration

## Description

Build the `/contact` page and wire it to Postmark, per
[[/Projects/django-migration/issues/Done/02-contact-email-provider|Contact-Form Email Provider]]
and the `ContactSubmission` model from ticket 12. Demoable as: a visitor
submits the contact form, the submission is persisted, and it's emailed to
the Swamp Monster inbox via Postmark.

## User Stories

10. As the site owner, I want every contact-form submission stored in the
    database in addition to being emailed to me, so that I still have a
    record if an email delivery fails.
14. As a visitor, I want to submit a contact form, so that I can reach out
    to the business.
15. As a visitor, I want my contact-form submission to reliably reach the
    business's inbox, so that I get a response.

## Implementation Plan Overview

- `django-anymail` configured with the Postmark backend; `EMAIL_BACKEND`
  settings mapped from `lib/swamp/mailer.ex` (per ticket 10's scaffolding).
- Contact form: `name`, `email`, `message` fields, server-side validation.
- On valid submission: create a `ContactSubmission` row, then send the
  notification email via Postmark. Persisting the DB row is independent of
  the email send succeeding — an email failure must not roll back or block
  the DB record.
- Contact page template: form + success/error states, single dark theme.
- Tests: form validation (invalid input rejected with errors shown),
  successful submission creates a `ContactSubmission` row and triggers a
  Postmark send via `django-anymail`'s test/dummy backend (no real email
  sent in CI), and an email-send failure still leaves the DB row intact.

## Acceptance Criteria

- [ ] `/contact` renders a form for `name`/`email`/`message` with
      server-side validation and error display.
- [ ] A valid submission creates a `ContactSubmission` row.
- [ ] A valid submission triggers a Postmark send via `django-anymail`.
- [ ] An email-send failure does not prevent or roll back the
      `ContactSubmission` row from being persisted.
- [ ] Tests cover validation, successful submission, and the
      email-failure-doesn't-block-persistence case, using Anymail's
      test/dummy backend.
