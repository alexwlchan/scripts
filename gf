#!/usr/bin/env bash
# Fetch any remote branches from the remote Git server.
#
# This includes removing any branches which have been deleted on the remote,
# e.g. when a GitHub pull request is merged.

set -o errexit
set -o nounset

git fetch origin --prune
