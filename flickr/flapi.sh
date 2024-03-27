#!/usr/bin/env bash
# A thin wrapper around the Flickr API.
#
# I use this to do quick inspection of API responses, e.g.
#
#     $ flapi flickr.photos.getInfo photo_id=52782497889
#

set -o errexit
set -o nounset

if (( $# == 1 ))
then
  method="$1"
  params=""
elif (( $# == 2 ))
then
  method="$1"
  params="$2"
else
  echo "Usage: $0 <METHOD> <PARAMS>" >&2
  exit 1
fi

api_key=$(keyring get flickr_api key)

curl --silent "https://api.flickr.com/services/rest/?api_key=${api_key}&method=${method}&${params}" \
  | ~/repos/scripts/text/pp_xml.sh
