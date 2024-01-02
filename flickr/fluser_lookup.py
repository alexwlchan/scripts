#!/usr/bin/env python3
"""
Look up a user by URL or path alias.

    $ fluser_lookup.py amymle
    ID:       '82621159@N00'
    username: 'amymle'
    realname: 'Amy Esau'

"""

import sys

from flickr_photos_api import FlickrPhotosApi
import keyring


if __name__ == "__main__":
    try:
        USER_TEXT = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <URL|PATH_ALIAS>")

    api = FlickrPhotosApi(
        api_key=keyring.get_password("flickr_api", "key"),
        user_agent="Alex Chan's personal scripts <alex@alexwlchan.net>",
    )

    if USER_TEXT.startswith("https://"):
        resp = api.call("flickr.urls.lookupUser", url=USER_TEXT)
    else:
        resp = api.call(
            method="flickr.urls.lookupUser",
            params={"url": f"https://www.flickr.com/people/{USER_TEXT}"},
        )

    user_id = resp.find(".//user").attrib["id"]
    username = resp.find(".//username").text

    resp = api.call(method="flickr.people.getInfo", params={"user_id": user_id})

    try:
        realname = resp.find(".//realname").text
    except AttributeError:
        realname = None

    print(f"ID:       {user_id!r}")
    print(f"username: {username!r}")
    print(f"realname: {(realname or '<none>')!r}")
