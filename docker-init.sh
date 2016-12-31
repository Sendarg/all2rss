#!/usr/bin/env bash

# ready for Redis
docker rm  rss-redis
docker run -d --name rss-redis -p 6379:6379 redis redis-server --requirepass vr2MD#a886d

# ready for Neo4j
mkdir -p $HOME/neo4j/data
docker rm  rss-neo4j
docker run -d --name rss-neo4j -p 7474:7474 -p 7687:7687 --volume=$HOME/neo4j/data:/data neo4j
curl -H "Content-Type: application/json" -X POST -d '{"password":"neo4j"}' -u neo4j:neo4j http://localhost:7474/user/neo4j/password

# Start Python
docker rm  all2rss
docker build -t all2rss .
docker run -d --name all2rss -p 2102:2102  --net=host  all2rss