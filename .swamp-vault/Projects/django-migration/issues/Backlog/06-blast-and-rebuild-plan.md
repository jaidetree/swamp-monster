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
