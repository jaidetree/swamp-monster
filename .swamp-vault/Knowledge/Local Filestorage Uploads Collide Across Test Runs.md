---
description: FileField uploads via local FileSystemStorage persist in MEDIA_ROOT across test runs (unlike the DB, which rolls back), so a hardcoded upload filename collides on a second run and Django appends a random suffix — assert against the saved name, not the literal
tags: [mistake]
date: 2026-08-22
---

A Playwright test (ticket 17) created a `Resource` via
`ResourceFactory(file__filename="pattern-template.zip", ...)` and asserted
the downloaded file's `suggested_filename == "pattern-template.zip"`. Passed
in isolation, failed when run as part of the full suite:
`'pattern-template_UNbMPKd.zip' != 'pattern-template.zip'`.

Cause: `MEDIA_ROOT` (local `FileSystemStorage`, the dev/CI fallback per
[[Conditional STORAGES Backend Keyed On Env Var Presence]]) is real disk
state that isn't wiped between test runs the way the Postgres test DB is
(pytest-django wraps each test in a transaction and rolls it back, but
never touches files a test wrote to disk). A prior run's leftover
`pattern-template.zip` was still on disk, so `get_available_name` appended
a random suffix on the second run's save — `file_overwrite` is only
configured for the R2 `S3Storage` backend, not the local fallback.

**Apply:** never hardcode an expected uploaded filename in an assertion;
derive it from the actually-saved `<field>.name` (e.g.
`resource.file.name.rsplit("/", 1)[-1]`) after the factory/`.save()` call.
Also fine to `rm -rf media/` between local test runs (it's gitignored,
`/media/` — pure scratch) if leftover files are just cluttering the
worktree, but the assertion fix is the real requirement since CI runners
are ephemeral and won't reliably reproduce the collision anyway.
