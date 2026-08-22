---
description: swamp/urls.py builds its local-media static() patterns once at import time from settings.DEBUG, so @override_settings(DEBUG=True) alone doesn't make MEDIA_ROOT fetchable in a live_server test — reload the urlconf module and clear_url_caches() too
tags: [mistake]
date: 2026-08-22
---

`swamp/urls.py` only appends `django.conf.urls.static.static(MEDIA_URL,
document_root=MEDIA_ROOT)` `if settings.DEBUG:` — production always serves
media from Cloudflare R2 (ticket 16), so this is dev-only convenience.
Ticket 17's Resource-download Playwright test needs the file actually
reachable over HTTP via `live_server`, but `urlpatterns` is a plain
module-level list built once when `swamp.urls` is first imported;
`@override_settings(DEBUG=True)` on a test flips the settings object but
never re-executes that module, so the local-media route still doesn't
exist.

**Apply:** for a test that needs this, flip `settings.DEBUG = True` (the
`settings` fixture auto-reverts it), then force a rebuild:
`importlib.reload(swamp.urls)` followed by
`django.urls.clear_url_caches()` (busts `get_resolver`'s cache, which is
keyed by the `ROOT_URLCONF` string and would otherwise keep resolving
against the stale pre-reload patterns). Revert both in a fixture's teardown.
Scope this to the one test that needs it — don't set `DEBUG=True` globally
for the whole suite.

Related: [[Pytest-Playwright Sync Api Trips Djangos Asyncio Guard]]
