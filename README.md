# Swamp Monster Leather

Django marketing site (migrated from Phoenix — see `legacy-elixir` branch
for the original). Empty scaffold stage: no CMS content/pages yet.

## Setup

```sh
nix develop        # Python 3.13, uv, Postgres 18, Node 24
uv sync             # install Python deps
npm install         # install Tailwind/esbuild CLIs
npm run build:css   # compile static_src/css/app.css -> static/css/app.css
```

## Local Postgres

Local dev/CI use a Nix-provisioned Postgres, not a system install or a
Docker service container:

```sh
export PGDATA="$PWD/.pgdata"
export PGHOST="$PWD/.pgsocket"
export PGDATABASE=swamp_dev
export PGPORT=5433
mkdir -p "$PGHOST"
./scripts/db start    # init + start; ./scripts/db stop / status also available
export DATABASE_URL="postgres://localhost:$PGPORT/$PGDATABASE"
```

## Run

```sh
uv run python manage.py migrate
uv run python manage.py runserver
```

Visit [`localhost:8000`](http://localhost:8000).

## Test / lint / type-check

```sh
uv run pytest
uv run mypy .
uv run ruff format --check .
uv run ruff check .
```

## Deploy

Hand-written `Dockerfile` (uv-based, `python:3.13-slim`), `fly.toml` targets
the staging Fly app `swamp-monster-leather-staging`. `fly deploy` requires
Fly credentials not available in every environment; see the ticket in
`.swamp-vault/Projects/django-migration/issues/Review/` for the manual
deploy steps.
