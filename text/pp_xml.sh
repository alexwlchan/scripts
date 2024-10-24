#!/usr/bin/env bash

set -o errexit
set -o nounset

# Check if we're running in a Terminal -- only pretty print the response
# with colours if so.
if [ -t 1 ]
then
  echo "terminal"
  xmllint --format - | pygmentize -l xml
else
  xmllint --format -
fi

