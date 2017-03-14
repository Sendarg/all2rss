#!/usr/bin/env bash

docker restart rss-redis
docker restart rss-neo4j
sleep 10
python start.py >./running.log 2>&1  &
exit
