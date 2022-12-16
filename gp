#!/usr/bin/env bash
# Pull any changes from the remote Git server.
#
# This includes removing any branches which have been deleted on the remote,
# e.g. when a GitHub pull request is merged.

set -o errexit
set -o nounset

if [[ "$1" == "--rebase" ]]
then
  git pull origin $(git rev-parse --abbrev-ref HEAD) --rebase
else
  git pull origin $(git rev-parse --abbrev-ref HEAD)
fi

git fetch origin --prune
