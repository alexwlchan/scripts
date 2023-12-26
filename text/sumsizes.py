#!/usr/bin/env python3
"""
Given a list of numbers on stdin, add them together and print the result
as a human-readable data size.

Example:

    echo -e '100 \n 201287 \n 3190817' | sumsizes

"""

import sys

import humanize


if __name__ == "__main__":
    total = sum(int(line) for line in sys.stdin.readlines())

    print(humanize.naturalsize(total))
