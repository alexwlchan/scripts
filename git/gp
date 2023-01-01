#!/usr/bin/env bash
# Pull any changes from the remote Git server.

set -o errexit
set -o nounset

if [[ "${1:-}" == "--rebase" ]]
then
  git pull origin $(git rev-parse --abbrev-ref HEAD) --rebase
else
  git pull origin $(git rev-parse --abbrev-ref HEAD)
fi

gf
