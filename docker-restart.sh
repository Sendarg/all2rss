#!/usr/bin/env bash

# ready for Redis
docker restart rss-redis
docker restart rss-neo4j
docker restart all2rss