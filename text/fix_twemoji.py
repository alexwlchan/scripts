#!/usr/bin/env python3
"""
When I copy/paste a tweet into Obsidian, often any emoji get replaced
by "twemoji" – links to Twitter’s custom emoji artwork.  e.g.

    "Oh damn I need this book!"![🤝](https://abs-0.twimg.com/emoji/v2/svg/1f91d.svg)

This script replaces those links with vanilla emoji characters.
"""

import sys

from fix_twitter_thread import fix_emoji


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <PATH>")

    with open(path) as in_file:
        text = in_file.read()

    text = fix_emoji(text)

    with open(path, "w") as out_file:
        out_file.write(text)
