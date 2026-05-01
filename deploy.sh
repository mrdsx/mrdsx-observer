#!/bin/bash

git fetch
git reset --hard origin/main

docker compose -f compose.prod.yaml up --build -d
