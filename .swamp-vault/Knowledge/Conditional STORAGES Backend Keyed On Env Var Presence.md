---
description: swamp-monster's pattern for env-optional storage backends — mutate STORAGES["default"] in settings.py only if all required env vars are present, so local/CI silently keep FileSystemStorage
tags: [pattern]
date: 2026-08-22
---

Ticket 16 (Cloudflare R2 media storage) needed a backend that's real in
production but untestable-for-real in this sandbox (no R2 credentials).
The pattern used: declare `STORAGES["default"]` as `FileSystemStorage` by
default, then after computing `R2_BUCKET_NAME = env("R2_BUCKET_NAME",
default=None)`, `if R2_BUCKET_NAME:` overwrite `STORAGES["default"]` with
the `storages.backends.s3.S3Storage` config (reading the other three R2 env
vars with no default, so a partially-set config raises loudly instead of
silently misconfiguring). Model fields never set `storage=` directly, so
they all pick up whichever backend `STORAGES["default"]` resolves to.

Testing this required no real R2/network access: `moto`'s `@mock_aws`
intercepts boto3 S3 calls in-process, so a test can construct
`storages.backends.s3.S3Storage(...)` with fake credentials and actually
`save()`/`open()`/`exists()` a file end-to-end. Reloading the `swamp.settings`
module (`importlib.reload`) under `monkeypatch.setenv`/`delenv` lets a test
assert the *conditional wiring itself* (which backend gets chosen) without
touching already-configured `django.conf.settings` global state.

**Apply:** reuse this shape for any other "real backend in prod, env vars
absent locally" wiring (e.g. a future email/SMS provider) — declare the
inert default first, gate the real backend behind `if <required_var>:`,
and test both branches by reloading the settings module under
monkeypatched env vars rather than mutating Django's live settings object.

Related: [[Envrc Is Intentionally Untracked In Swamp Monster]]
