---
tags:
    - wayfinder-map
---

# Django Migration

## Destination

Swamp Monster Leather is running on Django in this same repo (replacing the
never-launched Phoenix app — legacy code preserved on the `legacy-elixir`
branch), live by October 2026, with full parity to the existing
[[/Projects/swamp-monster-leather/Spec|Spec.md]]: Home, Contact, Works page, and
lightweight CMS contexts for works/training/resources, all content-editable
via Django admin.

## Notes

- Django is the settled target stack. Beacon (Elixir CMS) was tried and
  rejected as not mature enough — this is why we're leaving Phoenix, not a
  reopenable question on this map.
- Same repo, not a new one. `legacy-elixir` branch is the backup/reference
  point for the current (never-launched) Phoenix app; a worktree off it may
  be used while porting.
- Hosting is settled: Fly.io.
- Real content for Training/Resources/About is **not** this map's problem —
  the owner populates it through the CMS once it exists.
- Consult `docs/agents/issue-tracker.md` for vault/tracker conventions and
  `docs/agents/domain.md` for domain docs before resolving a ticket.

## Decisions so far

- [[/Projects/django-migration/issues/Done/01-placeholder-timing|Placeholder Timing]] — ship the
  "coming soon" placeholder today as a bare static page on Fly.io, no
  framework, independent of the Django migration; migration starts fresh
  separately.
- [[/Projects/django-migration/issues/Done/02-contact-email-provider|Contact-Form Email Provider]] — Postmark,
  via `django-anymail`'s Postmark backend.
- [[/Projects/django-migration/issues/Done/03-django-scaffolding-tooling|Django Scaffolding & Tooling]] —
  Python 3.13 / Django 5.2 LTS, `uv`, Nix devShell swapped to Python (keeping
  Postgres 18 + Node 24), Ruff + mypy/django-stubs, and the existing
  Tailwind v4 pipeline reused via CLI tools with daisyUI dropped in favor of
  a single inlined dark theme.
- [[/Projects/django-migration/issues/Done/04-cms-content-model|CMS Content Model]] — single
  `content` app with `Work` (+ `WorkImage` gallery), `Training`, `Resource`,
  and `ContactSubmission` models; `order`-driven admin via a ported
  `django-admin-sortable2` pattern from `~/projects/gracie`; Markdown text
  via `django-markdownify`; storage backend left to the Fly.io deployment
  ticket.
- [[/Projects/django-migration/issues/Done/05-fly-deployment-shape|Fly.io Deployment Shape]] —
  hand-written `uv`-based Dockerfile + gunicorn; `fly.toml` with
  `release_command` running migrations; Postgres via Crunchy Bridge
  ($10/mo, owner already provisions these directly) instead of Fly's own
  Postgres offerings; static files via WhiteNoise baked into the image;
  media (WorkImage uploads) via Tigris object storage + `django-storages`,
  no Fly Volume.

## Not yet specified

- DNS/cutover plan for pointing the live domain at the new Django deploy —
  now also needs to account for repointing DNS away from the placeholder's
  own Fly app (not just pointing DNS at Django for the first time); depends
  on the blast-and-rebuild plan.

## Out of scope

- Auth/user accounts (no user-facing login) — per the existing
  [[/Projects/swamp-monster-leather/Spec|Spec.md]].
- E-commerce/checkout — per the existing
  [[/Projects/swamp-monster-leather/Spec|Spec.md]].
