---
tags:
    - manual-testing
---

# Django Migration — Manual Testing Guide

This is the single manual-testing entry point for the whole Django migration.
Everything shipped to `Done/` was verified by an agent (tests, mypy, ruff, and
where possible live local checks) — this guide is for *your* pass: things
only a human can confirm (real browser rendering, drag-and-drop UX, live
credentials, production infra).

Ticket 18 (production cutover) is intentionally **not** in this guide as a
"Done" section — see [Stragglers](#stragglers) below, and
[[CUTOVER-RUNBOOK|CUTOVER-RUNBOOK.md]] for the live cutover steps.

## One-time setup

```bash
nix develop
uv sync
npm install && npm run build:css
./scripts/db start   # needs PGDATA/PGHOST/PGDATABASE/PGPORT set — see .github/workflows/ci.yml for the values CI uses
uv run python manage.py migrate
uv run python manage.py collectstatic --noinput
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Media uploads land under `MEDIA_ROOT` on local disk by default (no R2
credentials needed for local dev — see ticket 16 below).

## 09 — Blast Teardown & Python DevShell

1. In the main repo, run `nix develop` and confirm `python3 --version` →
   3.13.x, `uv --version`, `node --version` → v24.x, `postgres --version` →
   18.x — and that no Elixir/Erlang tooling is present in a *clean* shell
   (not one still holding an old direnv session).
2. Confirm `static/css/app.css`-equivalent source lives at
   `static_src/css/app.css` (ticket 10 later restructured this into a
   source/build split) and `assets/` no longer exists.
3. `cd ../swamp-monster-legacy-elixir` (sibling worktree), run `nix develop`,
   then `mix deps.get && mix phx.server` — confirm the original Phoenix app
   still boots, for parity comparisons against the new Django site.

## 10 — Django Scaffolding, CI & Staging Deploy

1. Confirm `manage.py runserver` boots locally (covered by the one-time
   setup above) and CI is green on GitHub once pushed (Actions tab → `CI`
   workflow → `pytest → mypy → ruff format --check → ruff check`, in order).
2. **Staging Fly app** — not yet provisioned in this pass (no Fly
   credentials were available while building). To do it yourself:
   - `fly apps create swamp-monster-leather-staging` (org `swamp-monster`)
   - Set at least `SECRET_KEY`, and `DATABASE_URL` once a staging Postgres
     exists (Crunchy Bridge or Fly Postgres — your call)
   - `fly deploy` from repo root; confirm the release command
     (`manage.py migrate --noinput`) runs and the app serves over HTTPS at
     its `.fly.dev` URL.
   - Note: `fly.toml`'s `app` now targets **production**
     (`swamp-monster-leather`) as of ticket 18's prep — see
     [[CUTOVER-RUNBOOK|CUTOVER-RUNBOOK.md]]. If you want to stand up staging
     again first, temporarily point `fly.toml` at
     `swamp-monster-leather-staging` for that deploy.

## 11 — Work Model & Sortable Admin

1. Log into `/admin/`. Under Content → Works, add a Work with a Markdown
   description (e.g. `**bold** and a [link](https://example.com)`), save,
   and confirm the rendered detail page (once you've published it) shows
   real HTML, not raw Markdown.
2. Add several gallery images inline, including via "Add another" *without*
   saving first — drag them into a new order (drag handle on the left),
   save, and confirm order persists. `order=1` is the thumbnail used
   elsewhere.
3. On the Work changelist, add 3+ Works and drag-reorder the list itself;
   confirm the order persists and stays gapless even after deleting one in
   the middle.
4. Toggle `published`/`featured` inline on the changelist — confirm they
   save immediately.

## 12 — Training, Resource & ContactSubmission Models & Admin

1. In `/admin/content/training/` and `/admin/content/resource/`: add an
   entry, confirm drag-to-reorder works and persists, confirm
   `published`/`featured` are inline-editable, edit `order` by hand on the
   change form, delete an entry.
2. On a `Resource`, upload a real file, open its admin change page, click
   the file link — confirm it downloads correctly.
3. Visit `/admin/content/contactsubmission/` — confirm there's no "Add"
   button and existing rows can't be opened for editing (read-only log).

## 13 — Works Page

1. Create a `Work` (Markdown description, a couple of `WorkImage`s with
   Markdown captions like `**bold**`/`_em_`), mark it `published`.
2. Visit `/works/` — confirm it appears; toggle `published=False` and
   confirm it disappears.
3. Click through to the Work's detail page — confirm gallery images show in
   admin-set order, captions render as formatted HTML, and the page stays
   in the single dark theme (no flash of unstyled content).

## 14 — Home Page

1. Visit `/` with an empty DB (no featured content yet) — confirm the hero
   renders and the Training/Resources sections don't look broken or leak
   any CMS-editor-facing placeholder text.
2. In `/admin/`, mark a few Works/Trainings/Resources both `published` and
   `featured`. Revisit `/` — confirm they now appear in their respective
   teaser sections, capped and ordered correctly.

## 15 — Contact Page & Postmark Integration

1. Visit `/contact/`, submit invalid input (e.g. empty message) — confirm
   inline field errors, no submission persisted.
2. Submit a valid entry — confirm the success state renders.
3. Check `/admin/content/contactsubmission/` — confirm the row was created.
4. **Real email delivery** wasn't verified in this pass (no Postmark
   credentials available). Once you have a Postmark server token:
   `fly secrets set POSTMARK_SERVER_TOKEN=... -a swamp-monster-leather`
   (see [[CUTOVER-RUNBOOK|CUTOVER-RUNBOOK.md]]), then re-submit `/contact/`
   on a deployed instance and confirm the notification actually lands in
   the Swamp Monster inbox.

## 16 — Media Storage: Cloudflare R2

1. Locally (no R2 env vars set), confirm uploads still work and land under
   `MEDIA_ROOT` on disk — this is the default dev behavior, by design.
2. Once you have R2 credentials: provision the bucket in the Cloudflare
   dashboard, create an API token, then set (locally, in `.envrc`, or as Fly
   secrets for production):
   - `R2_BUCKET_NAME`
   - `R2_ENDPOINT_URL` (`https://<account_id>.r2.cloudflarestorage.com`)
   - `R2_ACCESS_KEY_ID`
   - `R2_SECRET_ACCESS_KEY`
3. Upload a `WorkImage` (or `Training.image`/`Resource.icon`/`Resource.file`)
   with those vars set — confirm the file appears in the R2 bucket (via the
   Cloudflare dashboard or `aws s3 ls --endpoint-url ...`), not on local
   disk / the Fly machine's disk.
4. Confirm the saved model's `.url` resolves and serves the image correctly
   in a browser.
5. If deployed, restart the Fly machine and confirm a previously uploaded
   file is still retrievable (proving it survived off the ephemeral disk).

## 17 — Playwright E2E Golden Paths

1. `uv run playwright install chromium` if browsers aren't cached locally.
2. `uv run pytest tests/test_playwright_golden_paths.py -v` — confirm all
   four golden-path tests pass: Home → Works browsing, Work gallery
   viewing, Contact form submission (success state, no real email sent),
   Resource file download from the Home page's Resources footer section.
3. Push to a branch/PR and watch the GitHub Actions `CI` run — confirm the
   Playwright install/cache steps behave correctly in that environment (this
   couldn't be observed from the build sandbox).

## End-to-end pass

With a handful of Works/Trainings/Resources seeded and featured via admin:

1. Land on `/` — hero, featured Works grid, Training/Resources/About footer
   all render, single dark theme, no flash of unstyled content.
2. Click through Home → a featured Work → its full gallery.
3. Click "View the Portfolio" → `/works/` → browse the full listing → a
   Work detail page.
4. Download a Resource file from the Home footer.
5. Submit `/contact/` — see the success state; confirm the row shows up in
   admin.
6. Confirm nothing on any page references Elixir/Phoenix, and there's no
   daisyUI/light-theme flash anywhere.

## Stragglers

### 18 — Production Cutover (in `Review/`, not `Done/`)

Every acceptance criterion on this ticket is a real, irreversible action
against production infrastructure the site owner controls — deploying to
the live domain, setting production secrets, destroying the temporary
staging Fly app, and giving sign-off. None of that was attempted by an
agent. What *was* done safely:

- `fly.toml`'s `app` field now points at the real production app
  (`swamp-monster-leather`), not the staging one.
- A full runbook with the exact commands to run — secrets, deploy,
  verification, staging teardown, rollback — is written at
  [[CUTOVER-RUNBOOK|CUTOVER-RUNBOOK.md]].

Once you've run through it and the live domain is confirmed healthy, check
off ticket 18's boxes yourself and move it from `issues/Review/` to
`issues/Done/`.

Also worth reading before cutover: ticket 10's staging-deploy manual step
(above) was never actually run against a real staging app either — if you
want a dry run before touching production, provision staging first using
those steps.
