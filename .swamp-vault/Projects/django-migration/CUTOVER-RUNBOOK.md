# Production Cutover Runbook

Companion to
[[/Projects/django-migration/issues/Review/18-production-cutover|18-production-cutover]].
These are the exact commands the **site owner** runs by hand, in order, from
a machine with Fly credentials (`fly auth login` already done). None of this
was run by the agent that prepared this repo — it has no Fly, Crunchy
Bridge, Postmark, or R2 production credentials, and the steps below are
irreversible/live by nature.

`fly.toml` in the repo root already targets the production app
(`app = "swamp-monster-leather"`) — no `-a` flag is strictly needed, but the
commands below include it explicitly for safety since a stray `-a` mismatch
is a common way to hit the wrong app.

## 0. Prerequisites (must already be true)

- Cloudflare nameserver migration + R2 bucket provisioned (ticket 16).
- Crunchy Bridge production Postgres provisioned, `DATABASE_URL` in hand.
- Postmark production server token in hand.
- R2 production credentials in hand (bucket name, endpoint, access key,
  secret key).
- Tickets 09–17 all in Done.

## 1. Set production secrets

Run from the repo root:

```sh
fly secrets set \
  DATABASE_URL="postgres://..." \
  POSTMARK_SERVER_TOKEN="..." \
  R2_BUCKET_NAME="..." \
  R2_ENDPOINT_URL="https://<account-id>.r2.cloudflarestorage.com" \
  R2_ACCESS_KEY_ID="..." \
  R2_SECRET_ACCESS_KEY="..." \
  -a swamp-monster-leather
```

These are exactly the env vars `swamp/settings.py` reads (see
`DATABASE_URL` near the `DATABASES` setup, `R2_BUCKET_NAME` /
`R2_ENDPOINT_URL` / `R2_ACCESS_KEY_ID` / `R2_SECRET_ACCESS_KEY` in the R2
storage block, and `POSTMARK_SERVER_TOKEN` in the Anymail config). Setting
secrets on a Fly app does not itself trigger a deploy.

## 2. Deploy

```sh
fly deploy -a swamp-monster-leather
```

`fly.toml`'s `release_command` runs `manage.py migrate --noinput` before
the new machines take traffic. Fly's default blue-green strategy
health-checks the new Django machines and only swaps traffic once they're
healthy — zero visible downtime, no DNS change, since this is the same app
that already holds the live domain/certs.

## 3. Verify

- Open the live production domain in a browser.
- Click through the golden paths informally (home, works list/detail,
  contact form submit) — no formal smoke-test checklist per the resolved
  DNS/cutover ticket, just an eyeball check.
- Get explicit sign-off from the site owner before proceeding to step 4.

## 4. Destroy the temporary staging app

Only after production is confirmed healthy and signed off:

```sh
fly apps destroy swamp-monster-leather-staging
```

This is the throwaway app used during the port (ticket 10). It is not the
production app and destroying it does not touch the live domain.

## 5. Rollback (if step 2 or 3 goes bad)

Redeploy the placeholder to the same production app — another blue-green
swap, in reverse, no DNS surgery:

```sh
fly deploy -a swamp-monster-leather -c placeholder/fly.toml --dockerfile placeholder/Dockerfile
```

`placeholder/` (repo root) contains the original static placeholder site's
`fly.toml`, `Dockerfile`, `index.html`, `style.css`, and `logo.svg`. Keep
`placeholder/` in the repo until production Django is trusted — do not
delete it as part of this cutover.

Note: `placeholder/fly.toml` currently pins `primary_region = "iad"` while
the Django `fly.toml` uses `ewr`; the `-c` override above takes the
placeholder's own toml as-is, so this doesn't need reconciling before a
rollback.
