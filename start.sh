#!/usr/bin/env bash


# clean up
docker rmi -f $(docker images -qf "dangling=true")
docker stop all2rss && docker rmi -f all2rss && docker rm -f all2rss

# ready DB
./docker-readyDB.sh

# start All2Rss
python start.py