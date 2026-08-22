---
tags:
    - ready-for-agent
type: task
blocked_by:
    - "[[/Projects/django-migration/issues/Backlog/10-django-scaffolding-ci-staging-deploy|10-django-scaffolding-ci-staging-deploy]]"
---

# Work Model & Sortable Admin

## Description

Build the `content` Django app's first and most complex model, `Work`, with
its `WorkImage` gallery, per
[[/Projects/django-migration/issues/Done/04-cms-content-model|CMS Content Model]].
This slice establishes the sortable-admin pattern (ported from
`~/projects/gracie`) that the rest of the `content` app's models reuse.
Demoable as: the owner can log into Django admin, create a Work with a
Markdown description, add and drag-reorder gallery images (including
unsaved ones), and publish/feature it.

## User Stories

2. As the site owner, I want to add, edit, and delete Work entries (title,
   Markdown description, gallery images), so that I can showcase finished
   leather goods.
3. As the site owner, I want to drag-reorder Works in the admin list, so
   that I control the display order visitors see without editing numeric
   fields by hand.
4. As the site owner, I want to drag-reorder a Work's gallery images
   (including newly added, unsaved ones), so that the first image — the
   thumbnail used everywhere the Work appears without its full gallery —
   is the one I choose.
5. As the site owner, I want to mark a Work as `published` or unpublished,
   so that I can stage a piece before it's visible to visitors.
6. As the site owner, I want to mark a Work as `featured`, so that only
   selected pieces appear in the Home page teaser.

## Implementation Plan Overview

- Create the `content` Django app.
- `Work` model: `title`, `slug`, Markdown `description`, `published`
  (bool), `featured` (bool), `order` (int), timestamps.
- `WorkImage` model: `work` FK, `image`, Markdown `caption`, `order` —
  `order=1` is the thumbnail used wherever `Work` appears without its full
  gallery. `ImageField` declared storage-agnostically (concrete backend
  lands in the media-storage ticket).
- Port `django-admin-sortable2`'s `SortableAdminMixin` usage from
  `~/projects/gracie` (`portfolio/admin.py`, `portfolio/ordering.py`,
  `portfolio/sortable_admin.css`): `order` excluded from
  `list_display`/`list_editable` so the drag handle is the leftmost
  column, re-added via `get_fields` on the change form; a pure
  `renumber(rows, field="order")` helper reapplies after every drag via an
  overridden `_update_order`.
- `WorkImage` as a drag-sortable inline under the `Work` admin using
  gracie's `DragNewRowsInline` pattern so unsaved new rows are draggable.
- Wire `django-markdownify` for `description`/`caption` rendering
  (`{{ text|markdownify }}`, allowed-tags whitelist).
- Migrations for both models.

## Acceptance Criteria

- [ ] Owner can create/edit/delete a `Work` and its `WorkImage` gallery
      entries through Django admin.
- [ ] Drag-reordering `Work` rows in the admin list persists the new
      `order` via the ported `renumber()` helper.
- [ ] Drag-reordering `WorkImage` rows — including a newly added, unsaved
      row — persists the new `order`.
- [ ] `published`/`featured` toggles are editable in admin and covered by
      model-level tests for `published`/`featured`/`order` filtering.
- [ ] Markdown `description`/`caption` renders as HTML via
      `django-markdownify` with the allowed-tags whitelist enforced.
