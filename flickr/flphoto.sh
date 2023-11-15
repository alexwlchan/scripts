#!/usr/bin/env bash

set -o errexit
set -o nounset

if (( $# != 1 ))
then
  echo "Usage: $0 <PHOTO_ID>" >&2
  exit 1
fi

PHOTO_ID="$1"

flapi.sh flickr.photos.getInfo photo_id=$PHOTO_ID
