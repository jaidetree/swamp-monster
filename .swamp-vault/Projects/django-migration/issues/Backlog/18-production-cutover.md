---
tags:
    - ready-for-agent
type: task
blocked_by:
    - "[[/Projects/django-migration/issues/Backlog/16-media-storage-cloudflare-r2|16-media-storage-cloudflare-r2]]"
    - "[[/Projects/django-migration/issues/Backlog/17-playwright-e2e-golden-paths|17-playwright-e2e-golden-paths]]"
---

# Production Cutover

## Description

Execute the cutover plan from
[[/Projects/django-migration/issues/Done/08-dns-cutover-plan|DNS/Cutover Plan]]:
deploy Django directly into the existing `swamp-monster-leather` Fly app
(currently serving the placeholder), with zero downtime and no DNS change.
This is the final slice — everything upstream must already be verified
(models, pages, media storage, e2e coverage) before this runs against the
live domain.

**Owner-side prerequisite, external to this ticket's code work:** the
Cloudflare nameserver migration and R2 bucket provisioning (per ticket 16)
must be complete, with production R2 credentials available to set as Fly
secrets, before this ticket's deploy step can run.

## User Stories

24. As the site owner, I want the production Django deploy to run
    automatically on `fly deploy` with migrations applied via a release
    command, so that I don't have to SSH in to run `migrate` by hand.
26. As the site owner, I want the cutover from the placeholder to Django to
    happen with zero visible downtime and no DNS changes, so that visitors
    never see an outage or cert error.
27. As the site owner, I want a rollback path that redeploys the
    placeholder to the same Fly app, so that a bad Django deploy can be
    reverted quickly without DNS surgery.
28. As an engineer, I want the temporary staging Fly app used during the
    port destroyed once production is confirmed healthy, so that we're not
    paying for or maintaining an unused app.

## Implementation Plan Overview

- Point `fly.toml`'s `app` at the existing `swamp-monster-leather` app
  (no new app creation, no rename).
- Set production secrets on that app: Crunchy Bridge `DATABASE_URL`,
  Postmark API key, Cloudflare R2 credentials (from ticket 16).
- `fly deploy` — Fly's default blue-green release strategy health-checks
  the new Django machines, then atomically swaps traffic. No maintenance
  window, no DNS edit.
- Verify informally: check the live domain in a browser, get owner
  sign-off. No formal smoke-test checklist per the resolved ticket.
- Destroy the temporary staging Fly app (from ticket 10) once production
  is confirmed healthy.
- Confirm the rollback path works in principle: redeploying
  `placeholder/fly.toml` to the same app is the documented rollback,
  another blue-green swap in reverse. `placeholder/` stays in the repo
  until production is trusted.

## Acceptance Criteria

- [ ] `fly.toml` targets the existing `swamp-monster-leather` app; no new
      Fly app is created for production.
- [ ] Production secrets (Crunchy Bridge `DATABASE_URL`, Postmark key,
      Cloudflare R2 credentials) are set on that app.
- [ ] `fly deploy` completes a blue-green swap with zero downtime and no
      DNS change; the live domain serves the Django app in a browser
      check.
- [ ] The temporary staging Fly app is destroyed post-verification.
- [ ] The rollback path (redeploy `placeholder/fly.toml` to the same app)
      is documented and confirmed viable.
