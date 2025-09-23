#!/usr/bin/env python3
"""
Given the name of a file, apply SmartyPants to get nice typographical
quotes etc.
"""

import sys

import smartypants


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {__file__} PATH")

    path = sys.argv[1]

    with open(path) as in_file:
        old_text = in_file.read()

    attrs = smartypants.Attr.default | smartypants.Attr.u
    new_text = smartypants.smartypants(old_text, attrs)

    if new_text != old_text:
        with open(path, "w") as out_file:
            out_file.write(new_text)
