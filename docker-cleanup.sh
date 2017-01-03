#!/usr/bin/env bash


# clean up
docker rmi -f $(docker images -qf "dangling=true")
docker stop  rss-redis && docker rm  rss-redis
docker stop  rss-neo4j && docker rm  rss-neo4j
docker stop all2rss && docker rmi -f all2rss && docker rm -f all2rss
