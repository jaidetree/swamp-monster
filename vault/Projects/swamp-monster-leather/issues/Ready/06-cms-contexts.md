---
tags:
    - ready-for-agent
---
# CMS Contexts

## Description

Migrated from `docs/tasks/Swamp Monster Leather Tasks.md` (Phase 2 → Setup
CMS → Create Contexts). Research/prep is done; no context module or
migration exists yet — `lib/swamp.ex` is still the unmodified generator
boilerplate and `priv/repo/migrations/` is empty. Goal: a Phoenix context to
model site content (starting with "works"/projects) instead of hardcoding it
in templates.

## User Stories

- A maintainer should be able to manage works/projects content through the
  data layer instead of editing template markup directly.

## Implementation Plan Overview

- Generate a context (e.g. `mix phx.gen.context Projects Project projects
  title:string description:text image_path:string` — adjust fields to match
  what the home/works templates actually render).
- Run the resulting Ecto migration.
- Wire the home page works section and the works page (`05-works-page`) to
  read from this context instead of static markup.

## Acceptance Criteria

- [x] Read docs on Contexts
- [x] Read docs on Plug
- [x] Determine how to model content in DB
- [ ] Generate projects context
- [ ] Run ecto migration
