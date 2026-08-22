---
description: a task brief claiming a blocking prerequisite ticket is done should be verified against the tracker folder, not trusted
tags: [mistake]
date: 2026-08-22
---

Dispatched to run ticket 10 (django-scaffolding-ci-staging-deploy) with the
brief asserting ticket 09 (blast-teardown-devshell) — its `blocked_by`
prerequisite — was "already torn down... merged into main." The worktree
still had the full Elixir app (`lib/`, `mix.exs`, Elixir `flake.nix`) and
09's file was sitting in `Ready/`, not `Done/`. The brief was simply wrong
about repo state.

**Apply:** when a slice is `blocked_by` another ticket, check that ticket's
actual folder in the vault tracker (`Ready`/`In Progress`/`Done`) and spot-check
the repo for its claimed effects, before trusting a task description's claim
that it's already landed. If it isn't done, do it first as its own commit
before touching the dependent ticket — don't silently assume or ask and stall
on something this mechanically verifiable.
