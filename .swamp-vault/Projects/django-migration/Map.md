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
  media (WorkImage uploads) via `django-storages`, no Fly Volume — **amended
  by DNS/Cutover Plan**: Cloudflare R2 replaces Tigris, since the domain's
  nameservers are moving to Cloudflare anyway.
- [[/Projects/django-migration/issues/Done/06-blast-and-rebuild-plan|Blast-and-Rebuild Plan]] —
  teardown-first on `main` directly: slice 1 deletes all Elixir-only paths
  and swaps `flake.nix`/`.envrc` to Python/uv in one commit, moving the
  reusable `assets/` pieces along with it; a `legacy-elixir` worktree serves
  as the parity reference during the port instead of a dual-toolchain
  devShell; everything after is incremental, one commit per slice, no
  separate final-teardown slice; Fly deploys to a distinct staging app
  during the port — **superseded in part by DNS/Cutover Plan**: no fresh
  production app is created, Django is deployed directly into the existing
  `swamp-monster-leather` app that already serves the placeholder.
- [[/Projects/django-migration/issues/Done/07-testing-ci-approach|Testing/CI Approach]] —
  `pytest`/`pytest-django` + Playwright; GitHub Actions, bootstrapped via
  `nix develop` (no CI Postgres service container — a ported
  `~/projects/gracie/scripts/db` script starts local Postgres inside the
  Nix shell instead); single combined job ordered `uv sync` → tests →
  `mypy` → `ruff format` → `ruff check`; triggers on push/PR to `main`.
- [[/Projects/django-migration/issues/Done/08-dns-cutover-plan|DNS/Cutover Plan]] —
  no DNS change and no new app: the placeholder's existing Fly app is
  already named `swamp-monster-leather` and already holds the live certs,
  so cutover is just pointing `fly.toml` at that app and deploying —
  Fly's blue-green release strategy swaps traffic with zero downtime.
  Staging app destroyed once production is confirmed healthy; rollback is
  redeploying `placeholder/fly.toml` to the same app. Prerequisite:
  Cloudflare nameserver move + R2 bucket must land before this deploy.

## Not yet specified

## Out of scope

- Auth/user accounts (no user-facing login) — per the existing
  [[/Projects/swamp-monster-leather/Spec|Spec.md]].
- E-commerce/checkout — per the existing
  [[/Projects/swamp-monster-leather/Spec|Spec.md]].
