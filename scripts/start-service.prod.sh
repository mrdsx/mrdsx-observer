#!/bin/bash

if [ -z "$1" ]; then
    exit 1
fi

echo "Deploying $1..."

git fetch
git reset --hard origin/main

docker compose -f ../compose.prod.yaml up $1 --build -d

echo "Successfully deployed $1!"
