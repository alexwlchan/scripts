#!/usr/bin/env python3

import os
import pathlib
import shutil
import subprocess
import sys
import tarfile

import hyperlink


BACKUP_ROOT = pathlib.Path("/Volumes/Media (Sapphire)/backups/ao3")


def get_ao3_id(url: str) -> str:
    # e.g. 'https://archiveofourown.org/works/1234' ~> '1234'
    u = hyperlink.DecodedURL.from_text(url)

    if u.path[0] == "works" and u.path[1].isnumeric():
        return u.path[1]
    else:
        raise ValueError(url)


def save_ao3_url(url: str):
    ao3_id = get_ao3_id(url)

    # Check if the fic is already downloaded -- if it is, nothing to do.
    if any(
        name.startswith(f"{ao3_id}-") and name.endswith(".tar.gz")
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

    out_path = BACKUP_ROOT / f"{ao3_id}-{title}.tar.gz"

    with tarfile.open(out_path, "w:gz") as tf:
        tf.add(tmp_dir, arcname=ao3_id)

    shutil.rmtree(tmp_dir)

    print(f" ~> {out_path}")


def wget(*args):
    subprocess.call(["wget"] + list(args), stdout=subprocess.DEVNULL)


if __name__ == "__main__":
    for url in sys.argv[1:]:
        save_ao3_url(url)
