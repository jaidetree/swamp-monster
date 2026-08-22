---
tags:
    - ready-for-agent
---

# Django Migration — Spec

## Problem Statement

Swamp Monster Leather's marketing site was being built on Phoenix, but that
app never launched and Beacon (the Elixir CMS it was meant to use) turned
out not mature enough to build on. The owner needs the site live by October
2026 with full parity to the original site plan — Home, Contact, Works,
plus a lightweight CMS for Works/Training/Resources they can edit
themselves — but rebuilt on Django instead. Complicating the rebuild: a
bare "coming soon" placeholder already occupies the live production domain
and its Fly.io app (shipped independently, ahead of this migration), so the
new app has to take over that same domain without a DNS change or
downtime, and without leaving two throwaway placeholder efforts behind.

## Solution

Rebuild the site as a Django app in the same repo, replacing the
never-launched Phoenix app entirely (kept as a `legacy-elixir` branch for
reference, not deleted from history). The rebuild is a blast-and-rebuild:
one upfront commit tears down all Elixir-only paths and swaps the dev
environment to Python, then everything else — Django scaffolding, the
`content` app (Works/Training/Resources/contact), templates/views, deploy
config — lands incrementally, one commit per slice, directly on `main`. A
`legacy-elixir` worktree serves as the live parity reference during the
port. Content (Works, Training, Resources) becomes owner-editable through
Django admin, with drag-to-reorder controlling display order. The app
deploys to Fly.io, backed by Crunchy Bridge Postgres and Cloudflare R2 for
media, and cutover is a same-app blue-green Fly deploy: the existing
`swamp-monster-leather` Fly app (currently serving the placeholder) gets
`fly.toml` repointed at it and the Django app deployed directly in, so
traffic swaps with zero downtime and no DNS edit.

## User Stories

1. As the site owner, I want to log into Django admin, so that I can manage
   site content without touching code.
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
11. As a visitor, I want to see the Home page with a hero, a Works
    showcase, and footer teasers for Training/Resources/About, so that I
    get an overview of the brand and its offerings.
12. As a visitor, I want a dedicated Works page listing the full portfolio
    beyond the Home page teaser, so that I can browse all published work.
13. As a visitor, I want to view a Work's full image gallery with captions,
    so that I can see a piece from multiple angles.
14. As a visitor, I want to submit a contact form, so that I can reach out
    to the business.
15. As a visitor, I want my contact-form submission to reliably reach the
    business's inbox, so that I get a response.
16. As a visitor, I want to download a Resource file directly from the
    Resources section, so that I can use the template without extra steps.
17. As a visitor, I want the site to render only in its single dark theme
    with no flash of an unstyled/wrong theme, so that the brand experience
    is consistent.
18. As an engineer porting the app, I want a `legacy-elixir` worktree
    available alongside my Django work, so that I can compare against the
    original Phoenix implementation without juggling two toolchains in one
    devShell.
19. As an engineer, I want the Nix devShell to provide Python 3.13, `uv`,
    Postgres 18, and Node 24 out of the box, so that I don't need to
    install tooling manually to start working.
20. As an engineer, I want Ruff, mypy, and django-stubs wired in, so that
    lint/format/type errors are caught before merge.
21. As an engineer, I want a single CI job that runs tests, then mypy, then
    Ruff format/check, on every push and PR to `main`, so that functional
    regressions are caught before paying for style/lint checks.
22. As an engineer, I want CI to spin up a local Postgres inside the Nix
    shell rather than depend on a GitHub Actions service container, so
    that CI matches local dev exactly.
23. As an engineer, I want Playwright browsers cached in CI, so that CI
    runs stay fast across pushes.
24. As the site owner, I want the production Django deploy to run
    automatically on `fly deploy` with migrations applied via a release
    command, so that I don't have to SSH in to run `migrate` by hand.
25. As the site owner, I want media uploads (Work gallery images, Resource
    files) stored in Cloudflare R2 rather than on the Fly machine's disk,
    so that uploads survive redeploys and machine restarts.
26. As the site owner, I want the cutover from the placeholder to Django to
    happen with zero visible downtime and no DNS changes, so that visitors
    never see an outage or cert error.
27. As the site owner, I want a rollback path that redeploys the
    placeholder to the same Fly app, so that a bad Django deploy can be
    reverted quickly without DNS surgery.
28. As an engineer, I want the temporary staging Fly app used during the
    port destroyed once production is confirmed healthy, so that we're not
    paying for or maintaining an unused app.

## Implementation Decisions

**Stack & tooling** — Python 3.13, Django 5.2 (LTS), `uv` as the package
manager. `flake.nix`/`.envrc` swap from the Elixir/Erlang/`lexical` devShell
to `python313` + `uv`, keeping `postgresql_18` and `nodejs_24` (Tailwind/
esbuild CLIs still need Node); `.envrc` drops Elixir-specific vars
(`ECTO_IPV6`, `fish_history`) but keeps the Postgres ones. Ruff for lint and
format; mypy + `django-stubs` for type-checking (Astral's `ty` considered
and rejected for now — no first-class Django/ORM plugin support yet,
tracked upstream at astral-sh/ty#291, revisit once that lands). The
existing Tailwind v4 pipeline (`assets/css/app.css`, `assets/vendor/*`) is
reused as-is, driven by the standalone Tailwind CLI + esbuild CLI rather
than a Django-specific asset package, output to Django's
`STATICFILES_DIRS`. daisyUI is dropped entirely (unused beyond leftover
class names); a single dark theme's CSS custom properties are inlined
directly in `:root` — no theme-switching plugin, no light/dark toggle.

**Content model** — a single `content` Django app with four models:
`Work` (`title`, `slug`, Markdown `description`, `published`, `featured`,
`order`, timestamps) with a related `WorkImage` (`work` FK, `image`,
Markdown `caption`, `order` — the `order=1` image is the thumbnail used
wherever a `Work` appears without its full gallery); `Training` (same
shape as `Work` minus the gallery — single `image` instead); `Resource`
(`title`, `slug`, Markdown `description`, `icon` image, downloadable
`file`, `published`, `featured`, `order`, timestamps); `ContactSubmission`
(`name`, `email`, `message`, `created_at`) as a redundant persisted record
of every contact-form inquiry, independent of the email-delivery path.
Every list model carries an explicit `order` `PositiveIntegerField`
(excluded from `list_display`/`list_editable`, re-added via `get_fields` on
the change form) driven by `django-admin-sortable2`'s `SortableAdminMixin`,
ported from `~/projects/gracie`'s `portfolio/admin.py` /
`portfolio/ordering.py` / `portfolio/sortable_admin.css` pattern: a pure
`renumber(rows, field="order")` helper reapplies after every drag via an
overridden `_update_order`; `WorkImage` uses gracie's `DragNewRowsInline`
pattern so unsaved new gallery rows are draggable too. Markdown fields
(`description`, `WorkImage.caption`) render via `django-markdownify`
(`{{ text|markdownify }}`, allowed-tags whitelist) — no rich-text/WYSIWYG
editor. Display queries filter `published=True` ordered by `order`
ascending everywhere; the Home page teaser adds `featured=True` and a
limit. `order` is the single owner-controlled ranking — `created_at`/
`updated_at` are tracked but never drive display order. Storage backend is
declared storage-agnostically (`ImageField`/`FileField`) at the model
layer; the concrete backend is Cloudflare R2 (below).

**Migration mechanics** — work happens directly on `main`, no branch/
worktree for the port itself (neither Phoenix nor Django is deployed from
`main` today — only the independent placeholder app is live). Slice 1 is
teardown-first, one commit: delete `lib/`, `mix.exs`, `mix.lock`,
`config/`, `priv/`, `test/`, `.formatter.exs`; swap `flake.nix`/`.envrc` to
the Python/uv devShell target state in the same commit; `git mv` the
reusable parts of `assets/` (`css/app.css`, `vendor/*`) into their Django
static location — a move, not delete-then-resurrect (`assets/js/app.js`,
Phoenix LiveView glue, does not survive and is rewritten fresh when
needed). A separate git worktree checked out from `legacy-elixir` (its own
untouched Elixir `flake.nix`) serves as the on-demand parity reference
during the port. Everything after slice 1 is incremental, one commit per
slice: Django scaffolding (`manage.py`, a `swamp/` settings package —
Django's own project-name convention — mapping `lib/swamp/repo.ex` →
`DATABASES`, `lib/swamp/mailer.ex` → Anymail/Postmark `EMAIL_BACKEND`
config), the `content` app, templates/views, deploy config. No dedicated
final-teardown slice. A distinct staging Fly app is used during build/
testing.

**Deployment** — hand-written Dockerfile around `uv` (`fly launch`'s Django
detector assumes pip/Poetry, doesn't understand `uv.lock`): `python:3.13-
slim` base, `uv` binary copied from Astral's image, `uv sync --frozen`,
`collectstatic` at build time, gunicorn as entrypoint. `fly.toml`:
`[build]` + `[http_service]` (port 8000, `force_https`,
`min_machines_running = 0`) + `[deploy] release_command` running
`manage.py migrate`; no `[[mounts]]`, no `[[statics]]`. Postgres is
external-managed: Crunchy Bridge ($10/mo) — not Fly's unmanaged Postgres
(unsupported) or Fly Managed Postgres ($38/mo floor), and no Neon free-tier
stopgap since the owner provisions Crunchy Bridge directly. Static files: WhiteNoise, baked into the image at build time. Media
(`WorkImage`, `Resource.file`, `Resource.icon`, `Training.image` uploads):
Cloudflare R2 via `django-storages`'s S3-compatible backend — supersedes
an earlier Tigris recommendation, chosen because the domain's nameservers
are moving to Cloudflare anyway and the owner is consolidating on that
account. Email: Postmark via `django-anymail`'s Postmark backend, chosen
over Mailgun (100/day cap, mixed deliverability reputation) and Resend
(less deliverability track record) for its transactional-only reputation
and adequate free tier at this volume; plain SMTP ruled out for lacking
managed SPF/DKIM/deliverability tooling.

**Cutover** — no new Fly app and no DNS change. The placeholder's existing
Fly app is already named `swamp-monster-leather` (org `swamp-monster`) and
already holds the issued certs for the production domains, and DNS already
points at it. Cutover is: point `fly.toml`'s `app` at that existing app,
set production secrets on it (Crunchy Bridge `DATABASE_URL`, Postmark key,
Cloudflare R2 credentials), and deploy — Fly's default blue-green release
strategy health-checks the new machines then atomically swaps traffic,
zero downtime, no maintenance window. Verification is informal: a browser
check of the live domain plus owner sign-off, no formal smoke-test
checklist. The temporary staging app is destroyed once production is
confirmed healthy. Rollback is redeploying `placeholder/fly.toml` to the
same app — another blue-green swap in reverse; the `placeholder/` folder
stays in the repo until production is trusted, then is deleted from git
history. Prerequisite, blocking the production deploy (not the cutover
decision itself): the Cloudflare nameserver migration and R2 bucket
provisioning must land first, since media uploads need working storage
from go-live onward.

**Testing/CI** — `pytest` + `pytest-django` for the test suite, Playwright
for browser/e2e tests. GitHub Actions (`github.com:jaidetree/swamp-
monster`) bootstrapped via `DeterminateSystems/nix-installer-action` +
`DeterminateSystems/magic-nix-cache-action`; every CI step runs through
`nix develop -c <cmd>`, so CI gets the same uv/Postgres 18/Node 24 as local
dev. No GitHub Actions Postgres service container — instead,
`~/projects/gracie/scripts/db` (init/start via `pg_ctl`/`initdb`, driven by
`PGDATA`/`PGHOST`/`PGDATABASE`/`PGPORT`) is ported into this repo and used
to start local Postgres inside the Nix shell before tests run (only the
script is reused, not gracie's own CI shape, which uses a service
container). Single combined job, ordered `uv sync` → start local PG →
`pytest` (incl. Playwright) → `mypy` → `ruff format --check` →
`ruff check` — functional correctness gates before style. Playwright
browsers installed via `playwright install --with-deps`, cached with
`actions/cache` keyed on the Playwright version. Triggers: push and PR
against `main` (no long-lived feature branches, matching the direct-on-
`main` migration approach).

## Testing Decisions

- Tests should assert on external behavior (rendered page content, HTTP
  responses, database state, outbound email calls), not on internal
  implementation details of views/admin classes.
- `content` app: model-level tests for `Work`/`WorkImage`/`Training`/
  `Resource` `published`/`featured`/`order` filtering (the query behavior
  Home/Works rely on), and admin ordering tests for the ported
  `renumber()` helper and `SortableAdminMixin` drag behavior — prior art in
  gracie's `portfolio/admin.py` and its accompanying tests, which this
  pattern is ported from.
- View/template tests for Home (teaser queries, featured+published
  filtering, empty-state rendering for unpopulated Training/Resources),
  Works (full published listing), and Contact (form validation, success/
  error rendering).
- Contact form integration test: a valid submission creates a
  `ContactSubmission` row and triggers a Postmark send via
  `django-anymail`'s test/dummy backend (no real email sent in CI).
  Failure of the email send must not roll back or block the DB record.
- Playwright e2e coverage for the golden paths: browsing Home → Works,
  viewing a Work's gallery, submitting the contact form, downloading a
  Resource file.
- CI enforces `mypy`/django-stubs type-checking and Ruff format/lint on
  every push/PR, after the test suite passes.

## Out of Scope

- Auth/user accounts — no user-facing login, per the existing
  [[/Projects/swamp-monster-leather/Spec|Spec.md]].
- E-commerce/checkout, per the same existing Spec.md.
- Populating real Training/Resources/About content — the owner does this
  through the CMS once it exists; this migration only needs to support
  empty/placeholder states gracefully.
- Any DNS/domain-purchase work — the domain and its nameservers are the
  owner's existing setup; only the Cloudflare nameserver move (already
  decided, tracked as a deploy prerequisite) touches DNS.
- Light/light-dark theme toggle — single dark theme only.
- Rebuilding or reusing any Phoenix LiveView behavior (`assets/js/app.js`)
  — Django's request/response model doesn't need it; any new interactivity
  is built fresh.

## Further Notes

- Hard deadline: live by October 2026.
- Beacon (Elixir CMS) was evaluated and rejected as not mature enough —
  this is the reason for leaving Phoenix, not a reopenable question.
- The "coming soon" placeholder was shipped independently of this
  migration (bare static HTML, no framework) and is not itself part of
  this spec's scope — it's the thing this migration's cutover eventually
  replaces in place.
- The `legacy-elixir` branch is retained as the permanent backup/reference
  point for the never-launched Phoenix app, not deleted after the port.
- All eight discovery tickets behind this spec live in
  `.swamp-vault/Projects/django-migration/issues/Done/` (`01`–`08`); the
  project [[/Projects/django-migration/Map|Map.md]] indexes them under
  "Decisions so far."
