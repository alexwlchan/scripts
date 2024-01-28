#!/usr/bin/env python3
"""
Converts a number of bytes into a human-readable size.

    $ echo '32036032' | natsize
    32.0 MB

"""

import sys

import humanize


if __name__ == "__main__":
    print(humanize.naturalsize(sys.stdin.read()))
