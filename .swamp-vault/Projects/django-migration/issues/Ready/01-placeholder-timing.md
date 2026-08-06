---
tags:
    - ready-for-human
type: grilling
---

# Placeholder Timing

## Question

The owner needs a placeholder live today: logo + "Swamp Monster Leather:
Coming soon." Given the Django migration is settled and same-repo, should
that placeholder be:

(a) a plain static page shipped ASAP on whatever's fastest (current Phoenix
    app, or something outside it entirely), with the Django migration
    starting separately afterward, or

(b) the Django migration starting today, with the placeholder as the first
    page built on the new stack (meaning Django scaffolding has to happen
    before anything goes live)?

Weigh time-to-live-today against not building two throwaway placeholders.
