---
tags:
    - ready-for-agent
type: task
---

# Blast Teardown & Python DevShell

## Description

The first slice of the blast-and-rebuild plan: tear down every Elixir-only
path in one commit and swap the dev environment to Python/uv in the same
commit, per
[[/Projects/django-migration/issues/Done/06-blast-and-rebuild-plan|Blast-and-Rebuild Plan]].
This is a mechanical prefactor, not a user-facing slice — it clears the
ground so Django scaffolding has somewhere to land. A `legacy-elixir`
worktree is set up as the on-demand parity reference for the rest of the
port.

## User Stories

18. As an engineer porting the app, I want a `legacy-elixir` worktree
    available alongside my Django work, so that I can compare against the
    original Phoenix implementation without juggling two toolchains in one
    devShell.
19. As an engineer, I want the Nix devShell to provide Python 3.13, `uv`,
    Postgres 18, and Node 24 out of the box, so that I don't need to
    install tooling manually to start working.

## Implementation Plan Overview

- Delete `lib/`, `mix.exs`, `mix.lock`, `config/`, `priv/`, `test/`,
  `.formatter.exs` in one commit.
- In the same commit, swap `flake.nix`/`.envrc` to the Python/uv devShell
  target state: `python313` + `uv` replacing `elixir`/`erlang`/`lexical`,
  keeping `postgresql_18`, `nodejs_24`, `pgcli`, `openssl`. `.envrc` keeps
  the Postgres env vars, drops `ECTO_IPV6` and `fish_history`.
- `git mv` the reusable parts of `assets/` (`css/app.css`, `vendor/*`) into
  their eventual Django static location — a move, not delete-then-
  resurrect. `assets/js/app.js` (Phoenix LiveView glue) does not survive
  this move; it is not ported.
- Set up a separate git worktree checked out from `legacy-elixir` (its own
  untouched `flake.nix` still has the Elixir toolchain) for on-demand
  parity comparisons during the rest of the port.
- Work happens directly on `main` — no branch for the port itself.

## Acceptance Criteria

- [ ] `lib/`, `mix.exs`, `mix.lock`, `config/`, `priv/`, `test/`,
      `.formatter.exs` are removed from `main`.
- [ ] `nix develop` on `main` provides Python 3.13, `uv`, Postgres 18, and
      Node 24, with no Elixir/Erlang tooling present.
- [ ] `assets/css/app.css` and `assets/vendor/*` exist at their new
      Django-appropriate static location, moved (not recreated).
- [ ] A `legacy-elixir` worktree exists and its devShell still runs the
      original Phoenix app for comparison.
