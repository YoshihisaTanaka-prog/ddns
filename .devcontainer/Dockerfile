FROM mcr.microsoft.com/devcontainers/ruby:1-3.3-bookworm

RUN apt-get update && apt-get install -y dnsutils
# Install Rails
RUN su vscode -c "gem install rails webdrivers"
RUN su vscode -c "bundle config --global path vendor/bundle"
RUN su vscode -c "/usr/local/rvm/bin/rvm fix-permissions"