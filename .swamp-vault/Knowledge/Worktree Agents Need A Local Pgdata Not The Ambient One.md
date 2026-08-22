---
description: scripts/db in a worktree must get its own PGDATA/PGHOST/PGPORT — the ambient env vars point at the main checkout's shared Postgres cluster
tags: [mistake]
date: 2026-08-22
---

The ambient shell in this sandbox already has `PGDATA`/`PGHOST`/`PGDATABASE`/
`PGPORT` set, pointing at `/Users/j/projects/swamp-monster/postgres_data` —
the *main* checkout's cluster, not the worktree's. Running `./scripts/db
start` unmodified from a worktree would init/start against that shared
cluster instead of an isolated one, which is exactly the kind of git-adjacent
cross-worktree bleed a worktree-isolated agent shouldn't do.

**Apply:** before running `scripts/db` in a worktree, export worktree-scoped
values first, e.g. `PGDATA=$PWD/.pgdata PGHOST=$PWD/.pgsocket
PGDATABASE=swamp_test PGPORT=5433 ./scripts/db start` (mirrors CI's
`.github/workflows/ci.yml` env block). Stop the server and `rm -rf` those dirs
when done — they're scratch, not tracked.

Related: [[Sandbox Nix Develop Leaks Ambient Direnv PATH]]
