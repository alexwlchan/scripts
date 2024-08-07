#!/usr/bin/env python3
"""
This script prints a short table of the subdirectories with the most entries,
plus the total number of entries in a directory.  It's useful if I'm trying
to clean up a disk, and I'm looking for directories where I can make quick
and easy gains.

         37 fishconfig
         48 repros
         51 colossus-wheels
         70 services
        292 .git
    -------
        699

It's also useful for finding the directory that's making backup software
unhappy because there's lots of filesystem activity (e.g. `node_modules`).

I often use this in conjunction with DaisyDisk (https://daisydiskapp.com/),
which breaks down directories by size.

This script takes an optional argument, which is the path to the directory
to scan.  Running ``cdir`` will scan the current directory; ``cdir <DIR>`` will
scan the directory ``DIR``.

"""

import collections
import os
import sys

import tqdm


def count_entries_under(d):
    with tqdm.tqdm(desc=d, leave=False) as pbar:
        total = 1

        for _, dirnames, filenames in os.walk(d):
            update = len(dirnames) + len(filenames)

            total += update
            pbar.update(update)

        return total


if __name__ == "__main__":
    prefixes = collections.Counter()

    try:
        root = sys.argv[1]
    except IndexError:
        root = "."

    for e in os.listdir(root):
        pth = os.path.join(root, e)
        if os.path.isdir(pth):
            prefixes[e] = count_entries_under(pth)
        else:
            prefixes["."] += 1

    for prefix, count in reversed(prefixes.most_common()):
        print("%7d\t%s" % (count, prefix))

    home_display = os.path.abspath(root).replace(os.environ["HOME"], "~")

    print("-------")
    print("%7d\t%s" % (sum(prefixes.values()), home_display))
