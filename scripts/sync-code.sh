#!/bin/bash

echo "Syncing code..."

git fetch
git reset --hard origin/main

echo "Code synced successfully."
