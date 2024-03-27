#!/usr/bin/env bash

set -o errexit
set -o nounset

xmllint --format - | pygmentize -l xml
