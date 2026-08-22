---
tags:
    - ready-for-agent
type: task
blocked_by:
    - "[[/Projects/django-migration/issues/Backlog/10-django-scaffolding-ci-staging-deploy|10-django-scaffolding-ci-staging-deploy]]"
    - "[[/Projects/django-migration/issues/Backlog/11-work-model-sortable-admin|11-work-model-sortable-admin]]"
---

# Media Storage: Cloudflare R2

## Description

Wire the storage-agnostic `ImageField`/`FileField`s declared on `Work`/
`WorkImage`/`Training`/`Resource` to a concrete backend: Cloudflare R2 via
`django-storages`, per the amendment on
[[/Projects/django-migration/issues/Done/05-fly-deployment-shape|Fly.io Deployment Shape]]
(superseding the original Tigris recommendation). Demoable as: uploading a
`WorkImage` (or any other media field) through admin lands the file in the
R2 bucket, not on the Fly machine's disk.

Provisioning the R2 bucket itself and the Cloudflare nameserver migration
are owner-side prerequisites tracked as a deploy blocker (see ticket 18) —
this ticket is the code-side `django-storages` wiring, which can be
verified against a test/sandbox R2 bucket or credentials the owner
provides ahead of production cutover.

## User Stories

25. As the site owner, I want media uploads (Work gallery images, Resource
    files) stored in Cloudflare R2 rather than on the Fly machine's disk,
    so that uploads survive redeploys and machine restarts.

## Implementation Plan Overview

- Configure `django-storages`'s S3-compatible backend pointed at a
  Cloudflare R2 endpoint, credentials read from environment/Fly secrets
  (not committed).
- Set `DEFAULT_FILE_STORAGE`/`STORAGES` (Django 5.2 `STORAGES` setting) so
  all `ImageField`/`FileField` uploads (`WorkImage.image`,
  `Training.image`, `Resource.icon`, `Resource.file`) route through R2,
  while static files (Tailwind output) remain on WhiteNoise —
  storage backends are split by purpose, not unified.
- Document the required environment variables (endpoint, bucket, access
  key, secret key) for the deploy ticket to set as Fly secrets.
- Test: an uploaded file (via admin or a direct model save) is retrievable
  from the configured storage backend, using a test/sandbox bucket or a
  mocked S3-compatible backend in CI (no real R2 credentials committed to
  the repo or CI config).

## Acceptance Criteria

- [ ] All CMS media fields (`WorkImage.image`, `Training.image`,
      `Resource.icon`, `Resource.file`) save to and retrieve from the
      configured R2-backed storage, not local disk.
- [ ] Static files (Tailwind CSS output) remain served via WhiteNoise,
      unaffected by the media storage change.
- [ ] Required R2 environment variables are documented for the production
      cutover ticket.
- [ ] A test verifies upload/retrieval against a test/sandbox or mocked
      S3-compatible backend, with no real credentials in the repo or CI.
