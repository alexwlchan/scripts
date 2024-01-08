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
        user = api.lookup_user_by_url(url=USER_TEXT)
    elif re.match(USER_TEXT, "^[0-9]{7}@N[0-9]{2}$"):
        user = api.lookup_user_by_id(user_id=USER_TEXT)
    else:
        user = api.lookup_user_by_url(url=f"https://www.flickr.com/people/{USER_TEXT}")

    print(f"ID:       {user['id']}")
    print(f"username: {user['username']}")
    print(f"realname: {user['realname'] or '<none>'}")
    print(f"profile:  {user['profile_url']}")
    print(f"photos:   {user['photos_url']}")
