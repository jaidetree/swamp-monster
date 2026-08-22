---
description: keep EMAIL_BACKEND pinned to Postmark in settings.py; swap to Anymail's test backend with @override_settings per test, not a global test-settings override
tags: [pattern]
date: 2026-08-22
---

`swamp/settings.py`'s `EMAIL_BACKEND` stays
`anymail.backends.postmark.EmailBackend` unconditionally — no test-only
settings module, no env-var branch. Tests that need `django.core.mail.outbox`
assertions apply `@override_settings(EMAIL_BACKEND="anymail.backends.test.EmailBackend")`
on just the send-path tests (ticket 15's contact-form notification). This
keeps production config as the single source of truth (what actually ships is
what's exercised by default) while still letting specific tests opt into
Anymail's dummy backend for `mail.outbox` assertions — no real network call,
no `POSTMARK_SERVER_TOKEN` needed anywhere in dev/CI.

Confirmed the opposite failure mode works too: with the real Postmark backend
active and no token set, calling `send_mail` raises, but since the view
wraps the send in `try/except Exception: logger.exception(...)` *after*
`ContactSubmission.objects.create(...)`, the DB row still persists — verified
with a manual `runserver` + `curl` POST, not just in tests.

**Apply:** don't introduce a `swamp/settings/test.py` just to swap
`EMAIL_BACKEND` — reach for `@override_settings` on the handful of tests that
actually assert on `mail.outbox`.
