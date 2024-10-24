#!/usr/bin/env bash

set -o errexit
set -o nounset

if [ -t 1 ]
then
  echo "terminal"
  xmllint --format - | pygmentize -l xml
else
  xmllint --format -
fi

