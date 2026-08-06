---
tags:
    - ready-for-agent
---
# Works Page

## Description

Migrated from `docs/tasks/Swamp Monster Leather Tasks.md` (Phase 1 →
Implement works page). Not started — no `/works` route or controller action
exists yet (`lib/swamp_web/router.ex` only has `/` and `/contact`). The home
page already has a works teaser section to draw on for style; this page is
the full portfolio listing. Work images already exist under
`priv/static/images/works/`.

## User Stories

- A visitor should be able to view the full works/portfolio listing at
  `/works`, beyond the home page teaser.

## Implementation Plan Overview

- Add `get "/works", PageController, :works` to `lib/swamp_web/router.ex`.
- Add `works/2` action to `lib/swamp_web/controllers/page_controller.ex`.
- Add `lib/swamp_web/controllers/page_html/works.html.heex` (`PageHTML`
  already embeds `page_html/*` templates).

## Acceptance Criteria

- [ ] Define route to `PageController.works`
- [ ] Define HTML & styles
