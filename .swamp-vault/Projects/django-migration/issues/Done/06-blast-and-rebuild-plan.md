---
tags:
  - ready-for-human
type: task
blocked_by:
  - "[[/Projects/django-migration/issues/Ready/05-fly-deployment-shape|05-fly-deployment-shape]]"
---

# Blast-and-Rebuild Plan

## Question

Plan the mechanics of transitioning this repo from the Elixir/Phoenix app to
the new Django project: whether to work from a worktree off `legacy-elixir`
while porting, what order files get removed in (`lib/`, `assets/`, `mix.exs`,
`flake.nix`, etc.), and when the swap actually lands on `main`.

Blocked until the scaffolding/tooling decision and the Fly.io deployment
shape are known — can't plan the swap without knowing what's replacing what.

## Resolution

- **Where the work happens**: directly on `main`, no worktree/branch for the
  port itself. Safe because neither Phoenix nor Django is currently deployed
  anywhere from `main` — only the placeholder has a live Fly app, and it's
  independent.
- **Slice 1 — teardown first**: delete `lib/`, `mix.exs`, `mix.lock`,
  `config/`, `priv/`, `test/`, `.formatter.exs` in one commit. Same commit:
  swap `flake.nix`/`.envrc` straight to the Python/uv devShell (per Django
  Scaffolding & Tooling's target end-state — keep `nodejs_24`,
  `postgresql_18`, `pgcli`, `openssl`; drop `elixir`/`erlang`/`lexical`), and
  `git mv` the reusable parts of `assets/` (`css/app.css`, `vendor/*`) into
  their Django-appropriate static location — a move, not a delete-then-
  resurrect. `assets/js/app.js` (Phoenix LiveView glue) doesn't survive the
  move as-is; rewritten fresh when needed.
- **Parity reference during the port**: a separate git worktree checked out
  from `legacy-elixir` (its own untouched `flake.nix` still has the Elixir
  toolchain) — spun up on demand to run the live Phoenix app for comparison,
  no dual-toolchain juggling in `main`'s devShell.
- **Everything after slice 1 is incremental**, one commit per slice:
  scaffold Django (`manage.py`, `swamp/` settings package — Django's own
  project-name convention, not the third-party `config/`-style convention;
  `lib/swamp/{application,mailer,repo}.ex` maps into `swamp/settings.py`:
  `repo.ex` → `DATABASES`, `mailer.ex` → Anymail/Postmark `EMAIL_BACKEND`
  config, `application.ex` has no real equivalent), the `content` app (per
  CMS Content Model), templates/views, deploy config, etc. No dedicated
  final-teardown slice — teardown already happened in slice 1.
- **Fly app identity**: a distinct staging app name during build/testing
  (Fly has no native app-rename feature — confirmed via research). Once
  Django reaches parity and the DNS/cutover work is ready to execute, a
  fresh Fly app is created named `swamp-monster-leather`, reclaiming it
  after the placeholder app is destroyed; DNS then flips to it. Full DNS
  mechanics stay a separate concern, but this fixes the app-naming approach
  it builds on.
