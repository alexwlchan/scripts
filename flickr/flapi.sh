#!/usr/bin/env bash
# A thin wrapper around the Flickr API.
#
# I use this to do quick inspection of API responses, e.g.
#
#     $ flapi flickr.photos.getInfo photo_id=52782497889
#

set -o errexit
set -o nounset

if (( $# != 2 ))
then
  echo "Usage: $0 <METHOD> <PARAMS>" >&2
  exit 1
fi

method="$1"
params="$2"
api_key=$(keyring get flickr_api key)

curl "https://api.flickr.com/services/rest/?api_key=${api_key}&method=${method}&${params}"