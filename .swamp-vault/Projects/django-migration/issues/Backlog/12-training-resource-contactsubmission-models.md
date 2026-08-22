---
tags:
    - ready-for-agent
type: task
blocked_by:
    - "[[/Projects/django-migration/issues/Backlog/11-work-model-sortable-admin|11-work-model-sortable-admin]]"
---

# Training, Resource & ContactSubmission Models & Admin

## Description

Round out the `content` app with the remaining three models from
[[/Projects/django-migration/issues/Done/04-cms-content-model|CMS Content Model]],
reusing the sortable-admin pattern established in
[[/Projects/django-migration/issues/Backlog/11-work-model-sortable-admin|Work Model & Sortable Admin]].
Demoable as: the owner can manage Training and Resource entries in admin
the same way as Works, and every contact-form submission (once the Contact
page exists) persists as a `ContactSubmission` row.

## User Stories

7. As the site owner, I want to add, edit, reorder, and publish Training
   entries (title, Markdown description, image), so that I can build out
   training content at my own pace.
8. As the site owner, I want to add, edit, reorder, and publish Resource
   entries (title, Markdown description, icon image, downloadable file), so
   that I can offer downloadable templates to visitors.
9. As the site owner, I want Training and Resources to render gracefully
   when empty or placeholder-only, so that the site doesn't look broken
   before I've populated real content.
10. As the site owner, I want every contact-form submission stored in the
    database in addition to being emailed to me, so that I still have a
    record if an email delivery fails.

## Implementation Plan Overview

- `Training` model: same shape as `Work` minus the gallery — `title`,
  `slug`, Markdown `description`, single `image`, `published`, `featured`,
  `order`, timestamps. Reuses the `SortableAdminMixin`/`renumber()` pattern
  from ticket 11 (no inline gallery needed).
- `Resource` model: `title`, `slug`, Markdown `description`, `icon` image,
  downloadable `file`, `published`, `featured`, `order`, timestamps. Same
  sortable-admin pattern.
- `ContactSubmission` model: `name`, `email`, `message`, `created_at`. No
  `order`/sortable admin needed — it's a log, not owner-curated content.
  Admin registration is read-only/list-only (no create/edit needed by the
  owner).
- Migrations for all three models.
- Model-level tests for `published`/`featured`/`order` filtering on
  `Training`/`Resource`, matching the pattern from ticket 11's `Work`
  tests.

## Acceptance Criteria

- [ ] Owner can create/edit/delete/reorder `Training` and `Resource`
      entries through Django admin, mirroring the `Work` sortable-admin UX.
- [ ] `Resource.file` downloads correctly once retrieved via its
      storage-agnostic `FileField`.
- [ ] `ContactSubmission` rows are visible (read-only) in admin.
- [ ] `published`/`featured`/`order` filtering is covered by model-level
      tests for both `Training` and `Resource`.
