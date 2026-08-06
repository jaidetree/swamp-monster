---
tags:
    - wayfinder-map
---

# Django Migration

## Destination

Swamp Monster Leather is running on Django in this same repo (replacing the
never-launched Phoenix app — legacy code preserved on the `legacy-elixir`
branch), live by October 2026, with full parity to the existing
[[/Projects/swamp-monster-leather/Spec|Spec.md]]: Home, Contact, Works page, and
lightweight CMS contexts for works/training/resources, all content-editable
via Django admin.

## Notes

- Django is the settled target stack. Beacon (Elixir CMS) was tried and
  rejected as not mature enough — this is why we're leaving Phoenix, not a
  reopenable question on this map.
- Same repo, not a new one. `legacy-elixir` branch is the backup/reference
  point for the current (never-launched) Phoenix app; a worktree off it may
  be used while porting.
- Hosting is settled: Fly.io.
- Real content for Training/Resources/About is **not** this map's problem —
  the owner populates it through the CMS once it exists.
- Consult `docs/agents/issue-tracker.md` for vault/tracker conventions and
  `docs/agents/domain.md` for domain docs before resolving a ticket.

## Decisions so far

- [[/Projects/django-migration/issues/Done/01-placeholder-timing|Placeholder Timing]] — ship the
  "coming soon" placeholder today as a bare static page on Fly.io, no
  framework, independent of the Django migration; migration starts fresh
  separately.

## Not yet specified

- Testing/CI approach for the Django app — depends on the scaffolding/tooling
  decision (see the Django scaffolding & tooling ticket).
- DNS/cutover plan for pointing the live domain at the new Django deploy —
  now also needs to account for repointing DNS away from the placeholder's
  own Fly app (not just pointing DNS at Django for the first time); depends
  on the blast-and-rebuild plan.
- Whether the CMS content-editing experience needs its own prototype pass,
  once the content-model ticket resolves.

## Out of scope

- Auth/user accounts (no user-facing login) — per the existing
  [[/Projects/swamp-monster-leather/Spec|Spec.md]].
- E-commerce/checkout — per the existing
  [[/Projects/swamp-monster-leather/Spec|Spec.md]].
