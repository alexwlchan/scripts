#!/usr/bin/env bash
# Gets the latest version of safari.rs, the command-line tool I use
# to get URLs from my running web browser.
#
# See https://github.com/alexwlchan/safari.rs

set -o errexit
set -o nounset

_install-github-bin alexwlchan/safari.rs