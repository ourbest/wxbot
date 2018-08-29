#!/usr/bin/env bash

IMAGE=registry.cutt.com/p/wxbot

docker pull $IMAGE
docker rm -f wxbot
docker run -d \
    -v /data/wxbots:/data \
    -p 5000:5000 \
    --name wxbot \
    $IMAGE

