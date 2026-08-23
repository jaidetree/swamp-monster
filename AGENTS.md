# Swamp Monster Leather

Django 5.2 marketing site (migrated from Phoenix/LiveView — the original
Elixir app lives on the `legacy-elixir` branch and is not otherwise relevant
here).

## Stack

- **Django 5.2**, Python 3.13, deps managed with **uv** (`uv sync`, `uv run ...`).
- **Postgres**, project-local via `scripts/db` (Nix-provisioned, not a system
  install or Docker container) — `make db-start` / `db-stop` / `db-status`.
- **Tailwind v4** compiled with the Tailwind CLI through npm (`static_src/css/app.css`
  → `static/css/app.css`), not the Phoenix asset pipeline — `make css` / `css-watch`.
- **ruff** (lint + format), **mypy** with `django-stubs`, **pytest** with
  `pytest-django` + `pytest-playwright` for tests, `factory-boy` for fixtures,
  `moto[s3]` for mocking R2/S3 in tests.
- Media storage: Cloudflare R2 (S3-compatible, via `django-storages`) in
  production, falling back to local `FileSystemStorage` whenever the R2 env
  vars are unset — the case in local dev and CI. Config via `django-environ`
  (`.env`), email via `django-anymail` on Postmark. See `config/settings.py`.

Run `nix develop` first — it provides `uv`, `npm`, and Postgres.

## Project layout

- `config/` — the Django project package: `settings.py`, `urls.py`, `wsgi.py`.
  `DJANGO_SETTINGS_MODULE=config.settings`.
- `swamp/` — the one Django app, holding all business logic:
  - `models.py` — `Work`, `WorkImage`, `Training`, `Resource`,
    `ContactSubmission`: all owner-editable site content.
  - `admin.py`, `ordering.py` — the shared sortable-admin pattern (see below).
  - `views.py`, `forms.py` (contact form), `urls.py`, `apps.py` (`SwampConfig`).
  - `static/swamp/` — app-scoped static assets (e.g. admin JS/CSS for the
    sortable inline).
  - `tests/` — app-scoped unit tests: `test_models.py`, `test_views.py`,
    `test_admin.py`, `test_ordering.py`, `test_contact.py`,
    `test_home_view.py`, `test_markdownify.py`, `factories.py`.
- `templates/` — project-wide (not inside the app): `base.html` +
  `templates/swamp/*.html`.
- `tests/` — top-level, integration-level tests, kept flat (no unit/e2e
  subfolders): `test_smoke.py`, `test_media_storage.py` (Django test-client
  integration tests), `test_playwright_golden_paths.py` (Playwright browser
  e2e tests).
- No `core`/`common` app — nothing cross-cutting has needed one yet; don't
  create one preemptively.
- `docs/agents/` and `.swamp-vault/` — agent-facing docs and the project
  vault; see **Agent skills** below.

## The sortable-admin content pattern

`Work`, `Training`, and `Resource` are all owner-curated, drag-reorderable in
the Django admin. This is the one non-obvious architectural pattern in the
codebase — read this before adding a new sortable model or touching admin
ordering:

- Each model carries a plain `order = PositiveIntegerField`, excluded from
  `list_display` so `django-admin-sortable2`'s drag handle can occupy the
  leftmost column instead.
- `swamp/admin.py`'s `RenumberingSortableAdmin` is the shared base
  (`SortableAdminMixin` + `admin.ModelAdmin`) every sortable model's
  `ModelAdmin` subclasses. It overrides `_update_order` to renumber the
  *entire* collection 1..N after every drag — sortable2 only reindexes the
  dragged span, so gaps from deletes or add-at-end survive unless the whole
  collection is renumbered.
- `swamp/ordering.py`'s `renumber(rows, field="order")` is the pure function
  behind that: given an already-ordered sequence, it sets `field` to each
  row's 1-based position and returns only the rows that changed, ready for
  `bulk_update`. No DB or admin wiring — that's deliberate, so the actual
  renumbering logic has its own test surface (`swamp/tests/test_ordering.py`).
- `DragNewRowsInline` (also in `admin.py`) makes unsaved inline rows
  (e.g. `WorkImage` rows added via "Add another") drag-sortable before
  they're saved, via `inline_sortable_new.js`.
- This whole pattern was ported from `~/projects/gracie`'s `portfolio` app —
  check there first if you need prior art on a variant of the same problem.

Reuse `RenumberingSortableAdmin` for any new drag-reorderable content model;
don't reinvent per-model ordering logic.

## Dev workflow

```sh
make dev          # Django dev server + Tailwind watcher together
make migrate       # apply migrations
make superuser      # create an admin user
```

Before considering a change done, run:

```sh
make lint format typecheck test
```

(`ruff check`/`ruff format --check`, `ruff check --fix`/`ruff format`, `mypy .`,
`pytest`.) Run `make help` for the full target list.

## Agent skills

### Project vault

Vault at `.swamp-vault/`, home for knowledge notes, ADRs, and reference
material. See `docs/agents/vault.md`.

### Issue tracker

Vault at `.swamp-vault/Projects/<slug>/`, kanban via Obsidian Bases. See
`docs/agents/issue-tracker.md`.

### Triage labels

Roles applied as frontmatter `tags:` on vault issue files (no tracker
labels). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` + ADRs at `.swamp-vault/ADRs`. See
`docs/agents/domain.md`.
