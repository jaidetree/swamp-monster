---
tags:
    - ready-for-agent
type: task
blocked_by:
    - "[[/Projects/django-migration/issues/Backlog/13-works-page|13-works-page]]"
    - "[[/Projects/django-migration/issues/Backlog/14-home-page|14-home-page]]"
    - "[[/Projects/django-migration/issues/Backlog/15-contact-page-postmark|15-contact-page-postmark]]"
---

# Playwright E2E Golden Paths

## Description

Add browser-level end-to-end coverage for the golden paths across the now-
complete page set, per the Testing Decisions in
[[/Projects/django-migration/Spec|Spec.md]]. This is the last verification
slice before production cutover — it exercises the real rendered pages
rather than views/templates in isolation.

## User Stories

Cross-cutting across all visitor-facing stories (11–17): Home, Works,
Contact, Resource download, and the single-dark-theme rendering guarantee.

## Implementation Plan Overview

- Playwright test: browse Home → Works, confirming the Works showcase
  teaser links through correctly.
- Playwright test: view a Work's full gallery from the Works page.
- Playwright test: submit the Contact form end-to-end (using Anymail's
  test/dummy backend, no real email sent) and see the success state.
- Playwright test: download a Resource file directly from the Resources
  section.
- Confirm CI's Playwright browser caching (set up in ticket 10) still
  applies cleanly with the added test count.

## Acceptance Criteria

- [ ] Playwright covers: Home → Works browsing, Work gallery viewing,
      Contact form submission (success path), and Resource file download.
- [ ] All four golden-path tests pass in CI using the existing
      `playwright install --with-deps` + `actions/cache` setup.
- [ ] No real Postmark email is sent during the Contact form e2e test.
