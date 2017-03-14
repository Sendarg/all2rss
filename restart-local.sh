#!/bin/bash

kill -9 `ps -ef|grep start.py|grep -v grep|awk '{print $2}'`

#### all2rss
echo "== Start [weixin-rss-py]"
neo4j restart 
pkill redis-server

sleep 7
nohup redis-server /usr/local/etc/redis.conf  2>&1 &

cd /Users/neoo/PycharmProjects/all2rss
python start.py >./running.log   &
