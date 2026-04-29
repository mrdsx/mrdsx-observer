# mrdsx observer

## Description

A dashboard for monitoring my projects status.

## Starting up

## Development

```sh
bun dev                                 # Start frontend
uv run uvicorn src.main:app --reload    # Start backend
docker compose -f compose.dev.yaml up   # Start local Firebase and Redis
```

## Production

```sh
docker compose -f compose.prod.yaml up   # Start frontend, backend and Redis in production mode
```

We use Docker for frontend, backend and Redis because they're self-hosted. Firebase is deployed to cloud and doesn't require start up command.