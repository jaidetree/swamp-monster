---
tags:
    - ready-for-human
type: grilling
---

# Testing/CI Approach

## Question

Decide the testing and CI approach for the new Django app, now that the
scaffolding/tooling is settled (Python 3.13, Django 5.2, `uv`, Ruff,
mypy/django-stubs — see the
[[/Projects/django-migration/issues/Done/03-django-scaffolding-tooling|Django Scaffolding & Tooling]]
resolution):

- Test runner: Django's built-in test runner vs. `pytest` +
  `pytest-django`.
- What CI runs on push/PR (lint via Ruff, type-check via mypy, tests) and on
  what platform (GitHub Actions, Fly.io CI, etc.) — check what the current
  Elixir app's CI (if any) already does for a baseline.
- Whether/how the `uv` + Nix devShell setup needs to be mirrored in CI, or
  whether CI installs Python/deps a simpler way.

## Resolution

- **Test runner**: `pytest` + `pytest-django`, plus Playwright for
  browser/e2e tests.
- **CI platform**: GitHub Actions (repo is on
  `github.com:jaidetree/swamp-monster`). Baseline check: `legacy-elixir` has
  no CI config at all (no `.github/workflows`, no CircleCI) — green field,
  nothing to mirror.
- **Nix bootstrapping**: `DeterminateSystems/nix-installer-action` +
  `DeterminateSystems/magic-nix-cache-action` installs Nix on the runner;
  every step runs through `nix develop -c <cmd>`, giving CI the same
  uv/Postgres 18/Node 24 as local dev. `uv` manages Python deps directly
  (`uv sync`), not `pip`.
- **Postgres**: no GitHub Actions service container. Instead, port
  `~/projects/gracie/scripts/db` (init/start via `pg_ctl`/`initdb`, driven
  by `PGDATA`/`PGHOST`/`PGDATABASE`/`PGPORT`) into this repo and use it to
  start a local Postgres inside the Nix shell before tests run. Note this
  diverges from gracie's own `.github/workflows/ci.yml`, which actually uses
  a plain Postgres service container + `pip install` — only the local-PG
  script is being reused here, not gracie's CI shape.
- **Job shape**: a single combined job, ordered `uv sync` → start local PG →
  `pytest` (incl. Playwright) → `mypy` → `ruff format --check` →
  `ruff check` — functionality checked before style, so a broken test fails
  fast before paying for lint/format checks.
- **Playwright browsers**: installed via `playwright install --with-deps`,
  cached with `actions/cache` keyed on the Playwright version.
- **Triggers**: push and PR against `main` (matches the Blast-and-Rebuild
  Plan — direct-on-`main` development, no long-lived feature branches).
