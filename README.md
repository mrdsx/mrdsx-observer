# mrdsx observer

## Description

A dashboard for monitoring my projects status.

## Get started

### Development

Copy `.env.dev` to `.env` and fill in blank variables if needed for each directory:

- ./frontend
- ./backend
- ./webhooks/github

```sh
bun dev                                 # Start frontend
uv run uvicorn src.main:app --reload    # Start backend
docker compose -f compose.dev.yaml up   # Start local PostgreSQL and Redis
```

### Production

Copy `.env.prod` to `.env` and fill in blank variables if needed for each directory:

- ./frontend
- ./backend
- ./webhooks/github

Also, copy `.env.postgres.example` to `.env.postgres` in project root.

**Important note!**

Environment variables from `./.env.postgres` must be identical to variables from `./backend/.env` like so:

| `.env.postgres`     | `.env`        |
| ------------------- | ------------- |
| `POSTGRES_USER`     | `DB_USER`     |
| `POSTGRES_PASSWORD` | `DB_PASSWORD` |
| `POSTGRES_DB`       | `DB_NAME`     |

```sh
cd scripts
. ./start.prod.sh   # Run standalone script that'll start all necessary services
```

Production uses Docker for running self-hosted frontend, backend, PostgreSQL and Redis.
