---
description: pytest fails on any test that renders a Django admin page until collectstatic has run, because WhiteNoise's manifest storage has no manifest yet
tags: [pattern]
date: 2026-08-22
---

Adding admin-page tests for the `content` app's `Work` model (ticket
11-work-model-sortable-admin) surfaced a gap in `.github/workflows/ci.yml`:
the test job ran `uv sync` → `npm run build:css` → start Postgres → `pytest`,
but never ran `manage.py collectstatic`. Any test that renders a template with
a `{% static %}` tag — admin change/add pages are the obvious case — raised
`ValueError: Missing staticfiles manifest entry for '...'` from
`STORAGES["staticfiles"]` (`whitenoise.storage.CompressedManifestStaticFilesStorage`,
set in `swamp/settings.py`), because that backend resolves `{% static %}` URLs
against a manifest file that only `collectstatic` generates — it doesn't fall
back to the raw path like the plain filesystem backend does.

The Dockerfile already runs `collectstatic --noinput` at image build time, so
production/staging never hit this; only the test job was missing the
equivalent step.

**Apply:** any future `content` app ticket (Training, Resources, ...) that
adds admin tests inherits this fixed step — a "Collect static files" job runs
`nix develop -c uv run python manage.py collectstatic --noinput` right after
the Tailwind build and before Postgres starts. If a *new* CI job or workflow
is ever added that also renders admin templates (e.g. a separate lint/test
matrix), it needs the same step; don't assume `pytest` alone works.
