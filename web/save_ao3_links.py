#!/usr/bin/env python3

import os
import pathlib
import shutil
import subprocess
import sys

import hyperlink


BACKUP_ROOT = pathlib.Path("/Volumes/Media (Sapphire)/backups/ao3")


def get_ao3_id(url: str) -> str:
    # e.g. 'https://archiveofourown.org/works/1234' ~> '1234'
    u = hyperlink.DecodedURL.from_text(url)

    if u.path[0] == "works" and u.path[1].isnumeric():
        return u.path[1]
    elif (
        len(u.path) >= 4
        and u.path[0] == "collections"
        and u.path[2] == "works"
        and u.path[3].isnumeric()
    ):
        return u.path[3]
    else:
        raise ValueError(url)


def save_ao3_url(url: str):
    ao3_id = get_ao3_id(url)

    # Check if the fic is already downloaded -- if it is, nothing to do.
    if any(
        name.startswith(f"{ao3_id}-") and os.path.isdir(BACKUP_ROOT / name)
        for name in os.listdir(BACKUP_ROOT)
    ):
        return

    print(f"Saving {url}...")

    # Otherwise, create a temporary directory for the download.
    #
    # Delete any partial downloads first.
    tmp_dir = BACKUP_ROOT / f"{ao3_id}.tmp"

    try:
        shutil.rmtree(tmp_dir)
    except FileNotFoundError:
        pass

    for ext in ["azw", "epub", "mobi", "pdf", "html"]:
        wget(
            "--no-verbose",
            "--output-file",
            "-",
            # The Content-Disposition header is sent by the server to say
            # what the file "should" be called.  By telling wget to respect this,
            # it means we can request "a.html", the header from AO3 will specify
            # the correct filename (including the fic title), and the file will
            # be named correctly.
            "--content-disposition",
            "--directory-prefix",
            tmp_dir,
            f"https://archiveofourown.org/downloads/{ao3_id}/a.{ext}",
        )

    try:
        title = os.listdir(tmp_dir)[0].rsplit(".")[0]
    except FileNotFoundError:
        return

    out_dir = BACKUP_ROOT / f"{ao3_id}-{title}"

    os.rename(tmp_dir, out_dir)

    print(f" ~> {out_dir}")


def wget(*args):
    subprocess.call(["wget"] + list(args), stdout=subprocess.DEVNULL)


if __name__ == "__main__":
    for url in sys.argv[1:]:
        if url == "https://archiveofourown.org/series/136245":
            for story_url in [
                "https://archiveofourown.org/works/1854957",
                "https://archiveofourown.org/works/2089398",
                "https://archiveofourown.org/works/2218554",
                "https://archiveofourown.org/works/2249544",
                "https://archiveofourown.org/works/2330390",
                "https://archiveofourown.org/works/2399867",
                "https://archiveofourown.org/works/2467277",
                "https://archiveofourown.org/works/2802287",
            ]:
                save_ao3_url(story_url)
        else:
            save_ao3_url(url)
