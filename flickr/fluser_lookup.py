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

import re
import sys

from flickr_photos_api import FlickrPhotosApi
import hyperlink
import keyring


def get_user_id(user_text: str) -> str:
    u = hyperlink.URL.from_text(user_text)

    # e.g. https://www.youtube.com/watch?v=0naRXbQQ838
    if (
        u.host == "commons.flickr.org"
        and len(u.path) == 3
        and u.path[0] == "members"
        and u.path[2] == ""
    ):
        return {"path_alias": u.path[1]}


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
        user = api.lookup_user_by_id(
            url=f"https://www.flickr.com/people/{user_id['id']}"
        )

    print(f"ID:       {user['id']}")
    print(f"username: {user['username']}")
    print(f"realname: {user['realname'] or '<none>'}")
    print(f"profile:  {user['profile_url']}")
    print(f"photos:   {user['photos_url']}")
