#!/bin/bash

docker compose -f compose.prod.yaml up -d & disown
cd webhooks/github && nohup uv run uvicorn src.main:app --host 0.0.0.0 --port 8010 --reload > /dev/null 2>&1 & disown
