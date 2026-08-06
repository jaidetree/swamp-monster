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
