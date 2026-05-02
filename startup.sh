#!/bin/bash

cd ~/mrdsx-observer && docker compose -f compose.prod.yaml up -d & disown
cd ~/mrdsx-observer/webhooks/github && uv run uvicorn src.main:app --host 0.0.0.0 --port 8010 & disown
