#!/bin/bash

COMPOSE_FILE_PATH="./docker-compose.yml"

if [ ! -f "$COMPOSE_FILE_PATH" ]; then
        echo "docker-compose.yml not found at $COMPOSE_FILE_PATH"
        exit 1
fi

docker-compose down

echo "Pulling the latest image & updating container"
docker-compose pull
docker-compose up --force-recreate -d

echo "Erasing oldest image"
docker image prune -f

echo "Buggybot has been successfully updated"
