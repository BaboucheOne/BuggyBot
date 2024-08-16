#!/bin/bash

COMPOSE_FILE_PATH="./docker-compose.yml"

if [ ! -f "$COMPOSE_FILE_PATH" ]; then
        echo "docker-compose.yml not found at $COMPOSE_FILE_PATH"
        exit 1
fi

echo "Checking for updates..."

CURRENT_IMAGE_ID=$(docker-compose images -q)
docker-compose pull
PULLED_IMAGE_ID=$(docker-compose images -q)

if ["$CURRENT_IMAGE_ID" == "$PULLED_IMAGE_ID"]; then
        echo "No updates are available."
        exit 1
fi

echo "Now updating container."

docker-compose down
docker-compose up --force-recreate -d

echo "Erasing oldest image."
docker image prune -f

echo "Buggybot has been successfully updated."
