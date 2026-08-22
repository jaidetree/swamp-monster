---
description: `uv run <cmd>` in a Docker image auto-resyncs and installs the dev dependency group even after `uv sync --frozen --no-dev`, bloating the image
tags: [mistake]
date: 2026-08-22
---

Dockerfile ran `uv sync --frozen --no-dev` to install only production deps,
then used `uv run python manage.py collectstatic` and `CMD ["uv", "run",
"gunicorn", ...]`. Building the image showed `uv run` silently re-syncing and
installing the entire `dev` dependency group (mypy, ruff, playwright — tens of
MB) at that step, because `uv run` defaults to syncing the environment to
match the lockfile's full default groups, ignoring the `--no-dev` used
earlier in a separate `uv sync` call.

**Apply:** in a container that must ship without dev deps, don't invoke `uv
run` after the frozen/no-dev sync — call the venv's binaries directly
(`.venv/bin/python`, `.venv/bin/gunicorn`), or put `ENV PATH="/app/.venv/bin:$PATH"`
in the Dockerfile so plain `python`/`gunicorn` resolve without `uv` in the
loop at all. This also matters for Fly's `release_command`, which runs inside
the same image.
