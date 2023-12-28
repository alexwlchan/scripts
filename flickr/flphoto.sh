#!/usr/bin/env bash

set -o errexit
set -o nounset

if (( $# != 1 ))
then
  echo "Usage: $0 <PHOTO_ID>" >&2
  exit 1
fi

PHOTO_ID="$1"

if [[ "$PHOTO_ID" =~ ^[0-9]+$ ]]
then
  flapi.sh flickr.photos.getInfo photo_id=$PHOTO_ID
else
  PARSED_ID=$(flickr_url_parser "$PHOTO_ID" | jq -r .photo_id)

  if [[ "$PARSED_ID" =~ ^[0-9]+$ ]]
  then
    flapi.sh flickr.photos.getInfo photo_id=$PARSED_ID
  else
    echo "I don't know how to interpret $PHOTO_ID" >&2
    exit 1
  fi
fi
