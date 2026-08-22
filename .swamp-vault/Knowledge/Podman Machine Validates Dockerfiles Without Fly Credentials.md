---
description: podman machine init/start works in this sandbox and can build+run a real Dockerfile end-to-end, decoupling Dockerfile verification from Fly deploy access
tags: [pattern]
date: 2026-08-22
---

Needed to verify a hand-written Dockerfile (uv-based, WhiteNoise, gunicorn)
without any Fly.io credentials in the sandbox. `podman` was on PATH but had
no running machine (`Cannot connect to Podman ... no such file or directory`).
`podman machine init --disk-size 20` then `podman machine start` provisioned
and booted a Linux VM inside the sandbox in under two minutes, after which
`podman build`, `podman run -d -p <host>:<container>`, and `curl` against the
mapped port worked exactly like Docker would.

**Apply:** when a ticket needs Dockerfile/container verification but only
deploy credentials are missing, don't skip container verification entirely —
`podman machine init && podman machine start` first, then build/run/curl the
image locally. This caught a real bug (`uv run` re-installing dev deps at
runtime, see related note) that a syntax-only review would have missed.

Related: [[Uv Run Resyncs Dev Deps Even After Frozen No-Dev Sync]]
