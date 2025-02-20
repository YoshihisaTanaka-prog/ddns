#!/usr/bin/bash

cd $(dirname $0)
rm -f tmp/pids/server.pid && bundle config --global path vendor/bundle && bundle install && bundle exec rails s -b 0.0.0.0