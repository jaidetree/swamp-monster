---
tags:
    - ready-for-agent
type: task
blocked_by:
    - "[[/Projects/django-migration/issues/Backlog/11-work-model-sortable-admin|11-work-model-sortable-admin]]"
---

# Works Page

## Description

Build the `/works` page: the full portfolio listing beyond the Home page
teaser, per the existing
[[/Projects/swamp-monster-leather/Spec|Spec.md]]. Demoable as: a visitor
can browse every published `Work` in owner-controlled order and view a
Work's full image gallery with captions.

## User Stories

12. As a visitor, I want a dedicated Works page listing the full portfolio
    beyond the Home page teaser, so that I can browse all published work.
13. As a visitor, I want to view a Work's full image gallery with captions,
    so that I can see a piece from multiple angles.
17. As a visitor, I want the site to render only in its single dark theme
    with no flash of an unstyled/wrong theme, so that the brand experience
    is consistent.

## Implementation Plan Overview

- `/works` view: query `Work.objects.filter(published=True).order_by
  ("order")`, no `featured` filter (this is the full listing, unlike the
  Home teaser).
- Works listing template using the site's single dark theme, reusing the
  Tailwind pipeline from ticket 10.
- Work detail/gallery view rendering all `WorkImage`s in `order`, with
  Markdown `caption` rendered via `django-markdownify`.
- View/template tests: full published listing (respects `published`
  filter and `order`), gallery rendering.

## Acceptance Criteria

- [ ] `/works` lists every `published=True` `Work`, ordered by `order`
      ascending, excluding unpublished Works.
- [ ] Each Work's gallery view renders all its `WorkImage`s in `order`,
      with captions rendered as Markdown.
- [ ] View/template tests cover the `published` filter and gallery
      rendering.
