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
docker compose -f compose.prod.yaml up
```

Frontend needs Docker because it's self-hosted. Firebase and Redis are already deployed and do not require start up commands.