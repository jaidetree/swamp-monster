---
description: .envrc is a real, load-bearing devShell file in swamp-monster but is never git-tracked — edit it in place per-worktree, don't `git add` it
tags: [domain]
date: 2026-08-22
---

`swamp-monster`'s `.envrc` (direnv config pairing with `flake.nix`) sets
Postgres env vars for local dev but is not committed — `git ls-files` /
`git ls-tree` show it absent from every branch, and it's not even in
`.gitignore` (just never `git add`ed). Ticket 09 (blast-teardown-devshell)
described `.envrc` changes as part of "the same commit" alongside `flake.nix`,
but since it isn't tracked, those edits can't land in any commit — they're
a per-checkout local file.

**Apply:** when a ticket describes swapping `.envrc` content, create/edit the
file directly in the worktree (matching the target env vars) but don't try to
`git add` or commit it — that would silently change the repo's tracking
convention. Verify intent by checking `git ls-tree -r <ref> --name-only | grep
envrc` before assuming it should be tracked.

Related: [[Stale Origin Legacy-Elixir Branch Predates Teardown]]
