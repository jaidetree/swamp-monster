---
tags:
    - ready-for-agent
type: task
blocked_by:
    - "[[/Projects/django-migration/issues/Ready/09-blast-teardown-devshell|09-blast-teardown-devshell]]"
---

# Django Scaffolding, CI & Staging Deploy

## Description

Stand up an empty-but-real Django project on the tooling decided in
[[/Projects/django-migration/issues/Done/03-django-scaffolding-tooling|Django Scaffolding & Tooling]],
wire it into CI per
[[/Projects/django-migration/issues/Done/07-testing-ci-approach|Testing/CI Approach]],
and get it deploying to a distinct staging Fly app per
[[/Projects/django-migration/issues/Done/05-fly-deployment-shape|Fly.io Deployment Shape]].
This slice has no CMS content or pages yet — it's demoable as "an empty
Django app, lint/type/test-clean, auto-deployed to staging on push."

## User Stories

19. As an engineer, I want the Nix devShell to provide Python 3.13, `uv`,
    Postgres 18, and Node 24 out of the box, so that I don't need to
    install tooling manually to start working.
20. As an engineer, I want Ruff, mypy, and django-stubs wired in, so that
    lint/format/type errors are caught before merge.
21. As an engineer, I want a single CI job that runs tests, then mypy, then
    Ruff format/check, on every push and PR to `main`, so that functional
    regressions are caught before paying for style/lint checks.
22. As an engineer, I want CI to spin up a local Postgres inside the Nix
    shell rather than depend on a GitHub Actions service container, so
    that CI matches local dev exactly.
23. As an engineer, I want Playwright browsers cached in CI, so that CI
    runs stay fast across pushes.
24. As the site owner, I want the production Django deploy to run
    automatically on `fly deploy` with migrations applied via a release
    command, so that I don't have to SSH in to run `migrate` by hand.

## Implementation Plan Overview

- Scaffold `manage.py` and a `swamp/` settings package (Django's own
  project-name convention). Map `lib/swamp/repo.ex` → `DATABASES`,
  `lib/swamp/mailer.ex` → Anymail/Postmark `EMAIL_BACKEND` config.
- Add `pyproject.toml`/`uv.lock`, Ruff config, mypy + `django-stubs`
  config.
- Drive the existing Tailwind v4 pipeline via the standalone Tailwind CLI +
  esbuild CLI (a `manage.py` command or shell script), output to
  `STATICFILES_DIRS`. No daisyUI; single dark theme's CSS custom
  properties inlined in `:root`.
- Port `~/projects/gracie/scripts/db` into this repo for local
  Postgres init/start (`pg_ctl`/`initdb`, `PGDATA`/`PGHOST`/`PGDATABASE`/
  `PGPORT`).
- Add `pytest`/`pytest-django` + Playwright as test dependencies, with a
  minimal smoke test.
- Write the GitHub Actions workflow: `DeterminateSystems/nix-installer-
  action` + `magic-nix-cache-action`, every step through
  `nix develop -c <cmd>`, single job ordered `uv sync` → start local PG →
  `pytest` → `mypy` → `ruff format --check` → `ruff check`. Playwright
  browsers via `playwright install --with-deps`, cached with
  `actions/cache`. Triggers: push/PR to `main`.
- Hand-write a Dockerfile around `uv` (`python:3.13-slim`, `uv` binary
  copied from Astral's image, `uv sync --frozen`, `collectstatic` at build
  time, gunicorn entrypoint).
- Write `fly.toml` for a distinct staging app: `[build]` +
  `[http_service]` (port 8000, `force_https`, `min_machines_running = 0`)
  + `[deploy] release_command` running `manage.py migrate`. No
  `[[mounts]]`, no `[[statics]]`.
- Provision the staging Fly app and confirm `fly deploy` serves an empty
  Django app.
- Wire WhiteNoise for static files, baked into the image at build time.

## Acceptance Criteria

- [ ] `manage.py runserver` boots an empty Django project locally via
      `nix develop`.
- [ ] CI (GitHub Actions) runs on push/PR to `main` and passes: tests →
      mypy → Ruff format check → Ruff check, in that order, using a
      Nix-provisioned local Postgres.
- [ ] `fly deploy` against the staging app succeeds, runs migrations via
      the release command, and serves the app over HTTPS.
- [ ] Tailwind CSS builds and is served as a static asset via WhiteNoise.
