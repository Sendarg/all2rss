#!/usr/bin/env bash

# ready DB
./docker-readyDB.sh

# start All2Rss
python start.py >./running.log 2>&1  &