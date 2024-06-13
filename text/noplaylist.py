#!/usr/bin/env python3
"""
This script receives a YouTube URL on stdin, and removes the `list`
query parameter.

I use this in conjunction with `furl` and `youtube-dl`.  Sometimes
I want to download a single video from YouTube, but youtube-dl tries
to download an entire playlist.  This lets me grab just the first video.
"""

import sys

import hyperlink


if __name__ == "__main__":
    url = sys.stdin.read()
    url = hyperlink.parse(url)
    url = url.remove("list")
    sys.stdout.write(str(url))
