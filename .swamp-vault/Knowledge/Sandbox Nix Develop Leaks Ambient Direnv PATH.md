---
description: nix develop -c in this sandbox inherits a stale direnv PATH from the outer checkout, making `which <tool>` unreliable for verifying a devShell's actual contents
tags: [mistake]
date: 2026-08-22
---

After swapping `flake.nix`'s devShell from Elixir to Python/uv, `nix develop
-c bash -c 'which elixir'` still found `elixir`/`erl`/`lexical` on PATH — even
though they'd been removed from `buildInputs`. The sandbox's ambient shell env
carries `DIRENV_DIR`/`DIRENV_FILE` pointing at the *outer* shared checkout
(`/Users/j/projects/swamp-monster`, not the worktree), whose old Elixir
`flake.nix` had already been direnv-loaded into the session's PATH before my
worktree-scoped `nix develop` ran. `nix develop -c` layers its shell on top of
that ambient PATH rather than replacing it, so the contamination survives.

**Apply:** to get a trustworthy read of what a devShell actually provides,
strip the ambient PATH first: `PATH="/nix/var/nix/profiles/default/bin:/usr/bin:/bin:/sbin:/usr/sbin"
nix develop --command <cmd>`. A bare `which <tool>` inside an unscrubbed `nix
develop -c` is not proof of anything.
