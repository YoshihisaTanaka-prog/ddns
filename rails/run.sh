#!/usr/bin/bash

rm -f tmp/pids/server.pid && rails s -b 0.0.0.0
sleep infinity