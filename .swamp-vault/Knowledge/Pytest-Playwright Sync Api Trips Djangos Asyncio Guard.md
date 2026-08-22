---
description: pytest-playwright's sync `page` fixture falsely trips Django's SynchronousOnlyOperation guard around live_server/db setup; fix with DJANGO_ALLOW_ASYNC_UNSAFE=1
tags: [mistake]
date: 2026-08-22
---

Adding Playwright e2e tests (ticket 17) that combine `pytest-django`'s
`live_server` fixture with `pytest-playwright`'s sync `page` fixture failed
every test at db setup with `django.core.exceptions.SynchronousOnlyOperation:
You cannot call this from an async context`, raised from
`_django_db_marker` → `setup_databases` → `_nodb_cursor`. Reordering fixture
params (`live_server, page` vs `page, live_server`) had no effect.

Root cause: Playwright's sync API doesn't run its event loop in a separate
thread — it drives it via greenlet-based context switching in the *calling*
thread. That makes `asyncio.get_running_loop()` report a loop as running even
for otherwise-plain synchronous test code, which is exactly what Django's
async-safety guard (`django/utils/asyncio.py`) checks before allowing sync
ORM/db access. This is a false positive, not real concurrent access.

**Apply:** add a root `conftest.py` that sets
`os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "1")` — Django's own
documented escape hatch for exactly this class of false positive. No fixture
reordering or `pytest-playwright` config needed. Applies process-wide for the
whole pytest run, so no separate CI workflow change is needed either.

Related: [[Debug-Gated Media Urls Need Urlconf Reload For Live Server Tests]]
