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
[Django Scaffolding & Tooling](<../Done/03-django-scaffolding-tooling.md>)
resolution):

- Test runner: Django's built-in test runner vs. `pytest` +
  `pytest-django`.
- What CI runs on push/PR (lint via Ruff, type-check via mypy, tests) and on
  what platform (GitHub Actions, Fly.io CI, etc.) — check what the current
  Elixir app's CI (if any) already does for a baseline.
- Whether/how the `uv` + Nix devShell setup needs to be mirrored in CI, or
  whether CI installs Python/deps a simpler way.
