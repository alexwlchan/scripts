#!/usr/bin/env python3
"""
Download the photos from an Instagram post.
"""

import sys

import hyperlink
import instaloader


if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <URL>")

    url = hyperlink.DecodedURL.from_text(url)

    assert url.host == 'www.instagram.com', url
    assert url.path[0] == 'p', url

    post_id = url.path[1]

    L = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(L.context, post_id)
    L.download_post(post, post_id)
