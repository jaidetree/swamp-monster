---
name: slice
description: >-
  Use this skill when the user invokes /slice or wants to take one tracked
  vertical slice end-to-end: move it to In Progress, implement it, commit, and
  move it to Review. Trigger on "/slice <issue>", "do slice N", "work issue N",
  or "ship slice N".
---

# Slice

Take one tracked slice of Swamp Monster Leather end-to-end: In Progress → implement →
commit → Review.

Requires an issue argument (a `NN-slug` stem or number). Resolve it under
`.swamp-vault/Projects/swamp-monster-leather/issues/**` by filename stem (zero-pad numbers to
two digits) — the folder it sits in is its current dev state. If no argument, or
the target is ambiguous, stop and ask.

## Steps

1. Read `LEARNINGS.md` if it exists; surface the most relevant points.
2. Read the slice file, plus its PRD (`.swamp-vault/Projects/swamp-monster-leather/Spec.md`),
   `CONTEXT.md`, and any `.swamp-vault/ADRs` it touches. Stop if the issue isn't
   found — report what failed.
3. Move the slice file `Ready` → `In Progress` (folder = dev state; see
   `docs/agents/issue-tracker.md`).
4. `/implement` the slice as specified. Follow project conventions: one Phoenix
   context per module in `lib/swamp/`, LiveViews/controllers/components in
   `lib/swamp_web/`; follow AGENTS.md's Phoenix v1.8, Elixir, and LiveView
   guidelines (e.g. `<Layouts.app>` wrapper, `<.input>`/`<.icon>` components, no
   nested modules per file). Write/update tests at the seams the issue names.
5. Verify: `mix compile --warnings-as-errors` and `mix format --check-formatted`
   and `mix test`. On failure, fix and **goto 4**.
6. Commit: `/commit <slice description>`. Skip if nothing to commit; never
   commit partial or failing work.
7. Move the slice file `In Progress` → `Review` — this signals it awaits human
   testing. Check off the acceptance-criteria `- [ ]` boxes that now hold. Only
   a human moves it to `Done`.
8. Run `/update-learnings` to capture what worked, what broke, and non-obvious
   domain facts. Be selective.
9. Report a list of manual testing steps for humans.
