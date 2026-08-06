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

## Resolution

**Postmark**, integrated via `django-anymail`'s Postmark backend.

Context is low-volume (a small leather-goods contact form, not bulk mail),
and full DNS control is available for SPF/DKIM verification, so cost is a
non-issue across every candidate — all sit comfortably inside free/entry
tiers at this volume. Compared against Mailgun and Resend (researched 2026
pricing/features):

- **Mailgun**: forever-free tier but capped at 100/day rather than a clean
  monthly allotment; general-purpose sender with a more mixed deliverability
  reputation than transactional-only specialists.
- **Postmark**: transactional-only by design (no bulk/marketing traffic
  diluting reputation), strongest inbox-placement reputation of the three,
  free tier covers 100 emails/month — plenty for this form, plus free
  domain-health monitoring.
- **Resend**: newer/dev-first DX, roomiest free tier (3,000/mo), but less
  track record than Postmark's transactional-focused reputation.

Plain SMTP was ruled out earlier in the interview (no managed
SPF/DKIM/deliverability tooling — more fragile for a low-effort, low-volume
integration).

All three (and SendGrid) have well-established `django-anymail` backends, so
Django integration effort is roughly equal regardless of choice — Postmark
wins on deliverability fit for a low-volume transactional-only use case.
