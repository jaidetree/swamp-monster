---
tags:
    - ready-for-human
type: grilling
blocks:
    - "[06-blast-and-rebuild-plan](<../Backlog/06-blast-and-rebuild-plan.md>)"
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
