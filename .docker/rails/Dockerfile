FROM ruby:3.3
RUN apt-get update -qq && apt-get install -y postgresql-client sudo && gem install rails && bundle config --global path vendor/bundle
WORKDIR /app