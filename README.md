# mrdsx observer

## Description

A dashboard for monitoring my projects status.

## Get started

### Development

Copy `.env.dev` to `.env` and update the values as needed. Also make sure to obtain `service_account.json` file and paste it to the src directory.

```sh
bun dev                                 # Start frontend
uv run uvicorn src.main:app --reload    # Start backend
docker compose -f compose.dev.yaml up   # Start local Firebase and Redis
```

### Production

```sh
cd scripts
. ./start.prod.sh   # Run standalone script that'll start all necessary services
```

Production uses Docker for running frontend, backend and Redis because they're self-hosted. Firebase is deployed to cloud and thus doesn't need start up command.
