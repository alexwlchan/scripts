#!/usr/bin/env python3
"""
This script walks a directory tree, looks for empty directories,
and removes them.

It prints the name of every directory it removes.
"""

import os
import shutil
import sys

import humanize
import termcolor


def can_be_deleted(d):
    # This is a folder where I put files that I explicitly don't
    # want to put in backups.  See https://overcast.fm/+R7DX9_W-Y/21:22
    # or my Obsidian note about the same.
    if os.path.abspath(d) == "/Users/alexwlchan/Desktop/do not back up":
        return False

    entries = os.listdir(d)

    if not entries:
        return True

    if all(name in {".DS_Store", "__pycache__", ".venv"} for name in entries):
        return True

    return False


def delete_directory(d):
    assert can_be_deleted(d)
    print(d)
    shutil.rmtree(d)

    # Was this the only entry in its parent directory?  Unwind one level
    # to see if we can delete the parent also.
    parent = os.path.dirname(d)
    if can_be_deleted(parent):
        return 1 + delete_directory(parent)
    else:
        return 1


if __name__ == "__main__":
    total_deleted = 0

    try:
        root = sys.argv[1]
    except IndexError:
        root = "."

    for d, _, _ in os.walk(root):
        if can_be_deleted(d):
            total_deleted += delete_directory(d)

    if total_deleted == 1:
        print(termcolor.colored("1 directory deleted", "green"))
    elif total_deleted > 0:
        print(
            termcolor.colored(
                f"{humanize.intcomma(total_deleted)} directories deleted", "green"
            )
        )
    else:
        print(termcolor.colored("No empty directories found", "blue"))
