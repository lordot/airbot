#!/usr/bin/env bash

export TAG=$1
export REPO=$2
docker compose up -d --build
echo Docker compose started
