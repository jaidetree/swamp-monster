---
description: origin/legacy-elixir already existed at an old commit before slice 09 ran — branch from local main HEAD, not blindly reuse the remote ref
tags: [mistake]
date: 2026-08-22
---

Before slice 09 (blast-teardown-devshell) ran, `remotes/origin/legacy-elixir`
already existed, but pointing at a stale commit (`4146854`, predating the
`.swamp-vault` rename) — not a fresh cut of `main` right before teardown. Diffing
it against `main` showed no code differences, only vault-path renames, so it
was harmless but not what the ticket asked for ("create that branch first from
the current main HEAD").

**Apply:** when a ticket says "create branch X from current main HEAD," check
`git branch -a` first — if a same-named branch/remote-ref already exists,
don't assume it's already correct. Create/reset a *local* branch of that name
from `main` explicitly (`git branch legacy-elixir main`); local and
`remotes/origin/*` refs are distinct, so this doesn't collide. Pushing later
may need a force-push to reconcile with the stale `origin/legacy-elixir` —
flag that for whoever merges/pushes.
