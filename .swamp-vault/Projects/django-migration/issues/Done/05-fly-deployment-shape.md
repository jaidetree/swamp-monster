---
tags:
    - ready-for-agent
type: research
blocks:
    - "[06-blast-and-rebuild-plan](<../Backlog/06-blast-and-rebuild-plan.md>)"
---

# Fly.io Deployment Shape

## Question

Research how to deploy a Django app on Fly.io in 2026: Dockerfile pattern,
`fly.toml` config, Postgres (Fly Postgres vs. an external managed provider),
and static file serving (whitenoise vs. a CDN/object storage). Surface the
current recommended approach and tradeoffs so the blast-and-rebuild plan can
assume a concrete deployment shape.

Findings: `docs/research/fly-django-deployment.md` on the
`research/fly-deployment-shape` branch.

## Resolution

Recommended deployment shape:

- **Dockerfile**: hand-write it around `uv` (the `fly launch` Django
  detector assumes pip/Poetry and doesn't understand `uv.lock`) —
  `python:3.13-slim` base, `uv` binary copied in from Astral's image,
  `uv sync --frozen`, `collectstatic` at build time, gunicorn as the
  entrypoint.
- **fly.toml**: `[build]` + `[http_service]` (port 8000, `force_https`,
  `min_machines_running = 0`) + `[deploy] release_command` running
  `manage.py migrate`. No `[[mounts]]`, no `[[statics]]`.
- **Postgres**: skip both unmanaged Fly Postgres (Fly no longer supports it)
  and Fly Managed Postgres ($38/mo floor, oversized). Use an external
  managed provider — **Neon free tier** to start, **Crunchy Bridge ($10/mo)**
  as the upgrade path if autosuspend cold-starts become annoying.
- **Static files**: **WhiteNoise**, baked into the image at build time.
- **Media** (WorkImage gallery uploads): **Tigris** (Fly's native
  S3-compatible object storage) via `django-storages` — not a Fly Volume,
  since Fly's own guide steers media uploads toward S3-compatible storage
  instead.

Full sourcing and tradeoffs in the research doc above.
