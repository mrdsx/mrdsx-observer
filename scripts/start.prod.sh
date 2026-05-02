#!/bin/bash

cd $HOME/mrdsx-observer
docker compose -f compose.prod.yaml up -d & disown

cd $HOME/mrdsx-observer/webhooks/github
/usr/bin/nohup $HOME/.local/bin/uv run uvicorn src.main:app --host 0.0.0.0 --port 8010 > /dev/null 2>&1 &
