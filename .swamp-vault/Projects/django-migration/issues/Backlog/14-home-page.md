---
tags:
    - ready-for-agent
type: task
blocked_by:
    - "[[/Projects/django-migration/issues/Backlog/11-work-model-sortable-admin|11-work-model-sortable-admin]]"
    - "[[/Projects/django-migration/issues/Backlog/12-training-resource-contactsubmission-models|12-training-resource-contactsubmission-models]]"
---

# Home Page

## Description

Build the `/` Home page: hero, Works showcase, and footer teasers for
Training/Resources/About, per the existing
[[/Projects/swamp-monster-leather/Spec|Spec.md]]. Demoable as: a visitor
sees an overview of the brand with featured Works/Training/Resources, and
the page still renders sensibly when Training/Resources are empty.

## User Stories

9. As the site owner, I want Training and Resources to render gracefully
   when empty or placeholder-only, so that the site doesn't look broken
   before I've populated real content.
11. As a visitor, I want to see the Home page with a hero, a Works
    showcase, and footer teasers for Training/Resources/About, so that I
    get an overview of the brand and its offerings.
17. As a visitor, I want the site to render only in its single dark theme
    with no flash of an unstyled/wrong theme, so that the brand experience
    is consistent.

## Implementation Plan Overview

- `/` view: hero content (static/site-level, no CMS model), Works teaser
  query (`published=True, featured=True`, `order` ascending, limited to
  N), Training and Resource teaser queries with the same filter shape.
- Home template composing hero + Works showcase + Training/Resources/About
  footer sections, single dark theme.
- Empty-state handling: Training/Resources sections render gracefully
  (no broken layout, no CMS-editor-facing placeholder text) when no
  `featured=True, published=True` rows exist yet.
- View/template tests: featured+published filtering per section, and
  empty-state rendering when a section has zero qualifying rows.

## Acceptance Criteria

- [ ] `/` renders hero, Works showcase, and Training/Resources/About
      footer sections.
- [ ] Each teaser section queries `published=True, featured=True` ordered
      by `order`, limited to N.
- [ ] Training/Resources sections render without visual breakage when
      empty.
- [ ] View/template tests cover the teaser filtering and the empty-state
      case.
