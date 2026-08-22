---
description: WorkAdmin's get_fields/_update_order renumber-on-drag logic was extracted into a shared RenumberingSortableAdmin base the moment a second and third sortable model (Training, Resource) needed it
tags: [pattern]
date: 2026-08-22
---

Ticket 11 (Work) wrote its sortable-admin logic (`get_fields` re-adding
`order` on the change form, `_update_order` renumbering the whole collection
via `content.ordering.renumber`, the `sortable_admin.css` handle-width Media)
directly on `WorkAdmin`. Ticket 12 added `Training` and `Resource`, both
needing the identical behavior — copy-pasting it a second and third time
would have violated "no duplication" for logic that's genuinely
model-agnostic (it only touches `self.model`/`self.default_order_field`,
never `Work`-specific fields).

**Apply:** pulled the shared logic into `content.admin.RenumberingSortableAdmin(SortableAdminMixin,
admin.ModelAdmin)`; `WorkAdmin`, `TrainingAdmin`, `ResourceAdmin` now just
subclass it and add their own `inlines`/per-model bits. `content.ordering.renumber`
already anticipated this ("every sortable model in this app ... reuses this
single helper" — see its docstring) but the admin-layer wiring hadn't been
extracted yet. Any future sortable `content` model reuses `RenumberingSortableAdmin`
directly instead of re-deriving the pattern from `WorkAdmin`.
