#!/usr/bin/env python3

import datetime
import json
import pathlib

import httpx
import keyring


BACKUP_ROOT = pathlib.Path("/Volumes/Media (Sapphire)/backups/pinboard")


def get_bookmarks_json(username: str, password: str) -> str:
    """
    Call the Pinboard API to get a complete list of my bookmarks.

    Return the result as a pretty-printed JSON string.
    """
    resp = httpx.get(
        "https://api.pinboard.in/v1/posts/all",
        params={"format": "json"},
        auth=(username, password),
    )

    resp.raise_for_status()

    json_string = json.dumps(resp.json(), indent=2, sort_keys=True)

    return json_string


if __name__ == "__main__":
    username = "alexwlchan"

    password = keyring.get_password("pinboard", "password")
    assert password is not None

    json_string = get_bookmarks_json(username, password)

    now = datetime.date.today().strftime("%Y-%m-%d")

    for name in (f"bookmarks.{now}.json", "bookmarks.json"):
        with open(BACKUP_ROOT / name, "w") as outfile:
            outfile.write(json_string)
