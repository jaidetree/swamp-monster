---
tags:
    - ready-for-agent
type: research
blocks:
    - "[06-blast-and-rebuild-plan](<../Backlog/06-blast-and-rebuild-plan.md>)"
---

# Fly.io Deployment Shape

## Question

Research how to deploy a Django app on Fly.io in 2026: Dockerfile pattern,
`fly.toml` config, Postgres (Fly Postgres vs. an external managed provider),
and static file serving (whitenoise vs. a CDN/object storage). Surface the
current recommended approach and tradeoffs so the blast-and-rebuild plan can
assume a concrete deployment shape.

Findings: see the `research/fly-deployment-shape` branch (pointer added once
the research subagent completes).
