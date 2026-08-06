---
tags:
    - ready-for-human
type: grilling
---

# Contact-Form Email Provider

## Question

The current Phoenix app has Swoosh wired but no actual adapter configured —
the Mailgun config in `config/runtime.exs` is commented-out boilerplate, never
wired to a real account. Pick the email delivery provider/adapter the Django
contact form will use to deliver submissions to the Swamp Monster inbox
(e.g. Mailgun, Postmark, SendGrid, plain SMTP), weighing cost, deliverability,
and fit with a Fly.io-hosted Django app.
