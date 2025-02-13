FROM mcr.microsoft.com/devcontainers/ruby:1-3.3-bookworm

# Install Rails
RUN su vscode -c "gem install rails webdrivers"
RUN su vscode -c "/usr/local/rvm/bin/rvm fix-permissions"