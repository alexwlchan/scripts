#!/usr/bin/env python3
"""
Downloads and saves a single xkcd comic, plus a bit of metadata.

I'm not using this to create a complete archive of xkcd (of which I'm sure
many already exist) but to create a mini-library of my personal favourites.
"""

import json
import os
import pathlib
import sys
from urllib.request import urlretrieve

import httpx

BACKUP_ROOT = pathlib.Path("/Volumes/Media (Sapphire)/backups/xkcd")


if __name__ == "__main__":
    try:
        xkcd_number = int(sys.argv[1])
    except (IndexError, ValueError):
        sys.exit(f"Usage: {__file__} <XKCD_NUMBER>")

    resp = httpx.get(f"https://xkcd.com/{xkcd_number}/info.0.json")

    img_url = resp.json()["img"]
    filename = os.path.basename(img_url)
    name = os.path.splitext(filename)[0]

    try:
        with open(BACKUP_ROOT / f"{xkcd_number}-{name}.json", "x") as outfile:
            outfile.write(json.dumps(resp.json(), indent=2, sort_keys=True))
    except FileExistsError:
        pass

    out_path = BACKUP_ROOT / f"{xkcd_number}-{filename}"
    if not out_path.exists():
        urlretrieve(resp.json()["img"], out_path)
