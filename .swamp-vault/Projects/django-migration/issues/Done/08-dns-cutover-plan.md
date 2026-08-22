---
tags:
  - ready-for-human
type: grilling
blocked_by:
  - "[[/Projects/django-migration/issues/Done/06-blast-and-rebuild-plan|06-blast-and-rebuild-plan]]"
---

# DNS/Cutover Plan

## Question

Plan pointing the live domain at the new Django deploy, now that the
Blast-and-Rebuild Plan fixes the shape this depends on: a distinct staging
Fly app exists during the port, and the final production app gets created
fresh as `swamp-monster-leather` once Django reaches parity (Fly has no
app-rename, so this can't just be a rename of the staging app).

Needs to account for repointing DNS *away* from the placeholder's own Fly
app (not just pointing DNS at Django for the first time) — the placeholder
is live today on its own app/DNS pointer. Decide: the sequencing of
creating the final app vs. flipping DNS vs. destroying the placeholder and
staging apps, how much downtime (if any) is acceptable during the flip, and
whether a maintenance window or blue/green-style overlap is used.

## Resolution

**No DNS change and no new app.** Live facts checked at resolution time:
the placeholder's Fly app is *already* named `swamp-monster-leather` (org
`swamp-monster`), and it already holds the issued certs for
`swampmonsterleather.com` / `www.swampmonsterleather.com`. DNS already
points at that app's addresses. This means Done/06's assumption — that a
*fresh* app must be created as `swamp-monster-leather` because Fly has no
app-rename — doesn't need to hold: there's no rename involved, because the
target app name already exists as the live placeholder app.

**Cutover plan:**

1. Development continues on a separate temporary/staging Fly app during
   the port, as Done/06 already planned.
2. Cutover = point `fly.toml`'s `app` at the existing `swamp-monster-leather`
   app, set production secrets on it (Crunchy Bridge `DATABASE_URL`,
   Postmark key, Cloudflare R2 credentials — see amendment on
   [[/Projects/django-migration/issues/Done/05-fly-deployment-shape|05-fly-deployment-shape]]), and
   deploy. Fly's default blue-green release strategy spins up the new
   (Django) machines, health-checks them, then atomically swaps traffic —
   **zero downtime, no maintenance window, no DNS edit**.
3. Verification is informal: check the live domain in a browser, owner
   sign-off — no formal smoke-test checklist.
4. Destroy the temporary staging app once the production deploy is
   confirmed healthy.
5. Rollback = redeploy `placeholder/fly.toml` back to the same
   `swamp-monster-leather` app — just another release, same blue-green
   swap mechanism in reverse. The `placeholder/` folder stays in the repo
   (harmless) until production is trusted, then gets deleted from git
   history.

**Prerequisite (blocks the production deploy, not this decision):**
Cloudflare nameserver migration + R2 bucket provisioning must land before
the cutover deploy, since media uploads need working storage from go-live
onward. See the amendment on
[[/Projects/django-migration/issues/Done/05-fly-deployment-shape|05-fly-deployment-shape]].

**Supersedes part of** [[/Projects/django-migration/issues/Done/06-blast-and-rebuild-plan|06-blast-and-rebuild-plan]]:
that ticket's "fresh app created after placeholder destroyed" sequencing
is replaced by "deploy directly into the existing placeholder app" above.
