#!/usr/bin/env bash

# ready for Redis
docker run --name rss-redis -d redis redis-server --requirepass vr2MD#a886d

# ready for Neo4j
mkdir -p $HOME/neo4j/data
docker run --publish=7474:7474 --publish=7687:7687 -d --name rss-neo4j --volume=$HOME/neo4j/data:/data neo4j
curl -H "Content-Type: application/json" -X POST -d '{"password":"neo4j"}' -u neo4j:neo4j http://localhost:7474/user/neo4j/password

# Start Python
