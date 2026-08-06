---
tags:
    - ready-for-agent
---
# Contact Page

## Description

Migrated from `docs/tasks/Swamp Monster Leather Tasks.md` (Phase 1 →
Implement contact page). The original checklist is stale — `ContactController`,
`ContactHTML`, and the `/contact` route already exist
(`lib/swamp_web/controllers/contact_controller.ex`,
`lib/swamp_web/controllers/page_html/contact.html.heex`,
`lib/swamp_web/router.ex`). What's left: wire the form to actually submit and
send an email.

## User Stories

- A visitor should be able to submit the contact form and have it delivered
  to the Swamp Monster inbox.

## Implementation Plan Overview

- Update `lib/swamp_web/controllers/page_html/contact.html.heex` — the
  `<form>` has no `action`/`method`/CSRF token, so it doesn't currently POST
  anywhere.
- Update `lib/swamp_web/controllers/contact_controller.ex` `create/2` — it
  renders `:confirm` but never sends anything; wire it to `Swamp.Mailer`
  (`lib/swamp/mailer.ex`, Swoosh) to email the submission.

## Acceptance Criteria

- [x] Define ContactController
- [x] Define route to ContactController (`get`/`post "/contact"`)
- [x] Create HTML form & styles
- [ ] Form submits to `ContactController.create` (action/method/CSRF wired)
- [ ] Send email to swamp monster email on submit
