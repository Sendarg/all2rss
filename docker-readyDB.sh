#!/usr/bin/env bash

# ready for Redis
docker run -d --name rss-redis -p 6379:6379 redis redis-server --requirepass vr2MD#a886d


# ready for Neo4j
mkdir -p $HOME/neo4j/data
docker run -d --name rss-neo4j -p 7474:7474 -p 7687:7687 --volume=$HOME/neo4j/data:/data neo4j
sleep 10
curl -H "Content-Type: application/json" -X POST -d '{"password":"neo4321"}' -u neo4j:neo4j http://localhost:7474/user/neo4j/password
#sleep 1
#curl -H "Content-Type: application/json" -X POST -d '{"password":"neo4j"}' -u neo4j:neo4321 http://localhost:7474/user/neo4j/password