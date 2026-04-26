# mrdsx observer

## Description

A dashboard for monitoring my projects status.

## Starting up

## Development

```sh
bun dev                                # Start frontend
uv run uvicorn src.main:app --reload   # Start backend
docker compose up firebase redis       # Start local Firebase and Redis
```

## Production

```sh
docker compose up frontend    # Start frontend
uv run uvicorn src.main:app   # Start backend
```

Frontend needs Docker because it's self-hosted. Firebase and Redis are already deployed and do not require start up commands.