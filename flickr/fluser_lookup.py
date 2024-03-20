#!/usr/bin/env python3
"""
Look up a user by URL or path alias.

    $ fluser_lookup.py amymle
    ID:       82621159@N00
    username: amymle
    realname: Amy Esau
    profile:  https://www.flickr.com/people/amymle/
    photos:   https://www.flickr.com/photos/amymle/

"""

import sys
from typing import TypedDict

from flickr_photos_api import FlickrPhotosApi
from flickr_url_parser import is_flickr_user_id
import hyperlink
import keyring


class PathAlias(TypedDict):
    path_alias: str


class UserId(TypedDict):
    id: str


def get_user_id(user_text: str) -> PathAlias | UserId:
    # e.g. 35468159852@N01
    if is_flickr_user_id(user_text):
        return {"id": user_text}

    u = hyperlink.URL.from_text(user_text)

    # e.g. https://www.youtube.com/watch?v=0naRXbQQ838
    if (
        u.host == "commons.flickr.org"
        and len(u.path) == 3
        and u.path[0] == "members"
        and u.path[2] == ""
    ):
        return {"path_alias": u.path[1]}

    # e.g. "https://www.flickr.com/photos/35468159852@N01/"
    # e.g. https://www.flickr.com/photos/powerhouse_museum/2532449275/
    if u.host == "www.flickr.com" and len(u.path) >= 2 and u.path[0] == "photos":
        if is_flickr_user_id(u.path[1]):
            return {"id": u.path[1]}
        else:
            return {"path_alias": u.path[1]}

    raise ValueError(f"Cannot get Flickr user from {user_text!r}")


if __name__ == "__main__":
    try:
        USER_TEXT = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <URL|PATH_ALIAS>")

    api = FlickrPhotosApi(
        api_key=keyring.get_password("flickr_api", "key"),
        user_agent="Alex Chan's personal scripts <alex@alexwlchan.net>",
    )

    user_id = get_user_id(USER_TEXT)

    if "path_alias" in user_id:
        user = api.lookup_user_by_url(
            url=f"https://www.flickr.com/people/{user_id['path_alias']}"
        )
    else:
        user = api.lookup_user_by_id(user_id=user_id["id"])

    print(f"ID:       {user['id']}")
    print(f"username: {user['username']}")
    print(f"realname: {user['realname'] or '<none>'}")
    print(f"profile:  {user['profile_url']}")
    print(f"photos:   {user['photos_url']}")
