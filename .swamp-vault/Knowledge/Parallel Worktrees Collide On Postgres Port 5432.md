---
description: scripts/db in a fresh worktree fails to bind port 5432 if another worktree's Postgres is already listening there — reuse that instance's swamp_dev db instead of fighting for the port
tags: [pattern]
date: 2026-08-22
---

`scripts/db start` in a new worktree (ticket 16) failed with `could not bind
IPv4 address "127.0.0.1": Address already in use` — a different worktree's
Postgres (started earlier, same session tree) was already listening on
`127.0.0.1:5432`. Each worktree gets its own `PGDATA`/socket dir via
`.envrc`, but `DATABASE_URL`'s default (`postgres://localhost:5432/swamp_dev`)
is a plain TCP connection to `localhost:5432` — it ignores `PGHOST`/socket
path entirely, so it's really talking to whichever Postgres process holds
that shared port, not necessarily this worktree's own instance.

**Apply:** if `scripts/db start` fails with "Address already in use", don't
fight for the port — check `lsof -i :5432` for the other process, then just
`createdb -h localhost -p 5432 swamp_dev` against it (harmless if it already
exists) and proceed; pytest-django creates its own throwaway test DB
regardless. Only bother reassigning `PGPORT` if you actually need Postgres
data isolation between worktrees, which most tickets don't.

Related: [[Envrc Is Intentionally Untracked In Swamp Monster]]
