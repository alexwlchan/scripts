#!/usr/bin/env bash
# Pull any changes from the remote Git server.
#
# This includes removing any branches which have been deleted on the remote,
# e.g. when a GitHub pull request is merged.

set -o errexit
set -o nounset

git pull origin $(git rev-parse --abbrev-ref HEAD)
git fetch origin --prune
