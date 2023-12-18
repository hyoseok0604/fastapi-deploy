#!/bin/bash

docker compose -f ./docker/compose/docker-compose.yaml --project-directory . --env-file ./.env $@