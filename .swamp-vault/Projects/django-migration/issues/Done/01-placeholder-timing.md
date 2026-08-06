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

## Resolution

**(a) — bare static page, no framework at all, deployed to Fly.io today,
independent of the Django migration.**

- Neither the current Phoenix app nor a future Django app is faster than a
  plain static HTML+CSS page: hosting starts from zero either way (no
  existing Fly deploy or pipeline for this repo), and the placeholder needs
  new layout + a new logo asset, so nothing about Phoenix's existing
  homepage is reusable.
- Building the placeholder inside Phoenix would just be throwaway effort
  wrapped in a stack that's about to be deleted — worse than building it
  framework-free.
- The Django migration starts fresh and separately; this decision doesn't
  block it, so no execution ticket for building the placeholder goes on
  this map (it doesn't unblock any migration decision — see the map's
  Task-ticket rule).
- Consequence for later: the placeholder will live on its own Fly app with
  its own DNS pointer. The still-fogged DNS/cutover ticket needs to account
  for repointing DNS from the placeholder's Fly app to the Django one, not
  just pointing DNS at Django for the first time.
