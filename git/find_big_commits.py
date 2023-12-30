#!/usr/bin/env python3
"""
Give some information about the biggest files in the .git folder.

This is based on a Stack Overflow answer by raphinesse [1], with a bunch of
extra formatting and the total of the .git folder printed also.

[1]: https://stackoverflow.com/a/42544963/1558022

"""

import os
import subprocess

import humanize
import termcolor


def get_blobs():
    output = subprocess.check_output(
        "git rev-list --objects --all | "
        "git cat-file --batch-check='%(objecttype)\t%(objectname)\t%(objectsize)\t%(rest)'",
        shell=True,
    )

    for line in output.decode("utf8").splitlines():
        object_type, object_name, object_size, rest = line.split("\t")

        if object_type == "blob":
            yield {"commit_id": object_name, "size": int(object_size), "filename": rest}


def get_file_paths_under(root=".", *, suffix=""):
    """Generates the paths to every file under ``root``."""
    if not os.path.isdir(root):
        raise ValueError(f"Cannot find files under non-existent directory: {root!r}")

    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if os.path.isfile(os.path.join(dirpath, f)) and f.lower().endswith(suffix):
                yield os.path.join(dirpath, f)


def get_git_folder_size():
    root = (
        subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
        .decode("utf8")
        .strip()
    )

    return sum(
        os.path.getsize(p) for p in get_file_paths_under(os.path.join(root, ".git"))
    )


if __name__ == "__main__":
    blobs = [b for b in get_blobs() if b["size"] >= 1024]

    for b in sorted(blobs, key=lambda b: b["size"]):
        print(
            b["commit_id"][:7],
            humanize.naturalsize(b["size"]).rjust(10),
            "  ",
            b["filename"],
        )

    print(
        " " * 7,
        termcolor.colored(
            humanize.naturalsize(get_git_folder_size()).rjust(10), "blue"
        ),
        "  ",
        termcolor.colored(".git", "blue"),
    )
