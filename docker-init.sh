#!/usr/bin/env bash


# clean up
docker rmi -f $(docker images -qf "dangling=true")
docker stop  rss-redis && docker rm  rss-redis
docker stop  rss-neo4j && docker rm  rss-neo4j
docker stop all2rss && docker rmi -f all2rss && docker rm -f all2rss


# ready for Redis
docker run -d --name rss-redis -p 6379:6379 redis redis-server --requirepass vr2MD#a886d


# ready for Neo4j
mkdir -p $HOME/neo4j/data
docker run -d --name rss-neo4j -p 7474:7474 -p 7687:7687 --volume=$HOME/neo4j/data:/data neo4j


# Start Python
docker build -t all2rss .
#docker run -d --name all2rss -p 2202:2202 --link rss-neo4j --link rss-redis all2rss
docker run -d --name all2rss --net=host all2rss

# base config
curl -H "Content-Type: application/json" -X POST -d '{"password":"neo4321"}' -u neo4j:neo4j http://localhost:7474/user/neo4j/password