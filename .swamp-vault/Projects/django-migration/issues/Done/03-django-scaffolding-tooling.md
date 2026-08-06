---
tags:
  - ready-for-human
type: grilling
blocks:
  - "[[/Projects/django-migration/issues/Backlog/06-blast-and-rebuild-plan|06-blast-and-rebuild-plan]]"
---

# Django Scaffolding & Tooling

## Question

Decide the concrete tooling for the new Django project in this repo:

- Django and Python versions.
- Package/dependency manager (e.g. `uv`, `poetry`, plain `pip` + `requirements.txt`).
- Replacement for the current Elixir-flavored `flake.nix`/`.envrc` dev
  environment (Python equivalent via Nix, or drop Nix entirely).
- What happens to the existing Tailwind v4 pipeline (`assets/`) — reuse as-is
  against Django templates, or restructure for Django's static-file
  conventions.

This doesn't need to resolve the CMS content model or deployment specifics —
just the shape of the Django project itself.

## Resolution

- **Python/Django**: Python 3.13, Django 5.2 (LTS).
- **Package manager**: `uv`.
- **Nix**: keep `flake.nix`/`.envrc`, swap Elixir/Erlang/`lexical` for
  `python313` + `uv` in the devShell; keep `postgresql_18` and `nodejs_24`
  (Tailwind/esbuild CLIs still need Node). `.envrc` keeps the Postgres env
  vars, drops the Elixir-specific ones (`ECTO_IPV6`, `fish_history`).
- **Linter/formatter**: Ruff, for both.
- **Type-checker**: mypy + `django-stubs`. Considered Astral's `ty`
  (researched live) — it doesn't yet support Django's ORM/mypy-plugin
  patterns; Astral's own guidance is to stay on mypy for projects relying on
  `django-stubs`-style plugins until `ty` ships first-class Django support
  (tracked at [astral-sh/ty#291](https://github.com/astral-sh/ty/issues/291),
  targeted for `ty`'s 2026 stable release). Worth revisiting once that lands.
- **Tailwind pipeline**: reuse the Tailwind v4 CSS/config as-is
  (`assets/css/app.css`, `assets/vendor/*`), driven by the standalone
  Tailwind CLI + esbuild CLI (via a `manage.py` command or shell script)
  rather than a Django-specific asset package (`django-tailwind`, etc.).
  Output goes to Django's `STATICFILES_DIRS`, served via whitenoise — final
  call on whitenoise vs. a CDN belongs to the Fly.io Deployment Shape
  ticket.
  - **Drop daisyUI entirely.** Its component plugin was already commented
    out in `assets/css/app.css` (only the `daisyui-theme` color-token
    plugin was active) and templates only used leftover `btn`/`btn-ghost`
    class names with no real component behavior wired up — daisyUI wasn't
    pulling any weight. Branding calls for a single dark theme anyway, so
    no theme-switching plugin is needed.
  - **Single dark theme**, CSS custom properties inlined directly in
    `:root` (best practice) rather than routed through a theme plugin.
