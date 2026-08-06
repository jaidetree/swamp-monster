---
tags:
    - ready-for-human
type: grilling
---

# CMS Content Model

## Question

Design the Django data model behind the "lightweight CMS" the existing
[Spec.md](<../swamp-monster-leather/Spec.md>) calls for: content types for
Works (portfolio pieces), Training, and Resources (downloadable templates),
each manageable by the owner through Django admin without touching code.

Decide the models/fields (title, description, image(s)/file uploads,
ordering, etc.) and how they relate to the Home, Works, Contact pages.
Existing real work photos live at `priv/static/images/works/` and can inform
the Works shape; Training/Resources content is still placeholder and will be
populated by the owner later, so the model needs to support empty/placeholder
states gracefully.

## Resolution

Single `content` Django app, four models:

- **`Work`** — `title`, `slug`, `description` (Markdown text), `published`
  (bool), `featured` (bool), `order` (int), timestamps. Has a related
  **`WorkImage`** (`work` FK, `image`, `caption` Markdown text, `order`) — the
  gallery image at `order=1` is the thumbnail everywhere `Work` is shown
  without its full gallery.
- **`Training`** — same shape as `Work` minus the gallery: `title`, `slug`,
  `description` (Markdown), `image`, `published`, `featured`, `order`,
  timestamps.
- **`Resource`** — `title`, `slug`, `description` (Markdown), `icon` (image
  preview), `file` (the downloadable asset), `published`, `featured`,
  `order`, timestamps.
- **`ContactSubmission`** — `name`, `email`, `message`, `created_at`.
  Persists every contact-form inquiry as a redundant record (spam-pattern
  analysis, resilience if the email send fails). Does **not** replace the
  existing Postmark/`django-anymail` decision in
  [[/Projects/django-migration/issues/Done/02-contact-email-provider|Contact-Form Email Provider]] —
  that decision was about deliverability (SPF/DKIM, dedicated sending
  domain, bounce handling), which is unaffected by the form being
  single-recipient.

**Ordering & admin UX**: an explicit `order` `PositiveIntegerField` on every
list model (including `WorkImage`), driven by `django-admin-sortable2`'s
`SortableAdminMixin`. Ports the pattern from `~/projects/gracie`
(`portfolio/admin.py`, `portfolio/ordering.py`, `portfolio/sortable_admin.css`):

- `order` excluded from `list_display`/`list_editable` so the drag handle
  renders as the leftmost column.
- `order` re-added via `get_fields` on the change form so it's still
  manually editable per row.
- A ported `renumber(rows, field="order")` helper (pure function, ordered
  rows → position 1..N, returns only changed rows) reapplies after every
  drag via an overridden `_update_order`, closing the gaps that deletes and
  the add-at-end default otherwise leave.
- The ported CSS narrows the sortable2 drag-handle column and cleans up
  inline-row spacing.
- `WorkImage` is a drag-sortable inline (gracie's `DragNewRowsInline`
  pattern) under the `Work` admin, so unsaved new rows are draggable too.

**Display queries**: the full listing for each model (e.g. `/works`) filters
`published=True`, ordered by `order` ascending. The Home page teaser for
each uses the same filter plus `featured=True`, same `order`, limited to N.
No separate "newest" sort anywhere — `order` is the single, owner-controlled
ranking; `created_at`/`updated_at` are tracked but don't drive display order.

**Markdown**: `description` (and `WorkImage.caption`) are stored as plain
Markdown text and rendered via `django-markdownify` (wraps
`python-markdown`, gives a `{{ text|markdownify }}` filter with an
allowed-tags whitelist). No rich-text/WYSIWYG editor.

**Storage backend intentionally undecided here**: fields are declared as
Django's storage-agnostic `ImageField`/`FileField`. Local disk vs. Fly
volume vs. object storage is [[/Projects/django-migration/issues/Ready/05-fly-deployment-shape|Fly.io Deployment Shape]]'s
call, not this ticket's.

**Contact page**: no CMS-managed content relation beyond `ContactSubmission`
above — the form itself isn't editable-content.
