#!/bin/bash

if [ -z "$1" ]; then
    exit 1
fi

echo "Deploying $1..."
sleep 3
echo "Successfully deployed $1!"
