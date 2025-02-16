#!/usr/bin/bash

cd $(dirname $0)
rm -f tmp/pids/server.pid && rails s -b 0.0.0.0
sleep infinity