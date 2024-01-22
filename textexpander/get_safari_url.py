#!/usr/bin/python3

import os
import subprocess
import sys

import httpx

from urls import get_safari_url


def normalise_url(url: str) -> str:
    # If this is a URL at http://localhost:5757, it's probably the
    # local web server for Jekyll running my personal site.
    #
    # Rather than printing the raw URL, print the {% post_url %} syntax
    # required to do an inter-site link in Jekyll.
    if url.startswith("http://localhost:5757/"):
        *_, year, slug, _ = url.split("/")

        matching_files = [
            f
            for f in os.listdir(
                f"/Users/alexwlchan/repos/alexwlchan.net/src/_posts/{year}"
            )
            if f.endswith(f"{slug}.md")
        ]

        if len(matching_files) == 1:
            return (
                "{% post_url "
                + f'{year}/{matching_files[0].replace(".md", "")}'
                + " %}"
            )

    # If this is a URL at http://localhost:5959/, it's probably the
    # local web server for my book tracker.
    #
    # Rather than printing the raw URL, print a relative URL that's safe
    # to use in published links.
    if url.startswith("http://localhost:5959/"):
        return url.replace("http://localhost:5959", "")

    # If it's a Mastodon post, we want to retrieve the URL of the original
    # post rather than the copy of it on my server.
    if url.startswith("https://social.alexwlchan.net") and not url.startswith(
        "https://social.alexwlchan.net/@alex/"
    ):
        r = httpx.head(url)

        try:
            return r.headers["location"]
            sys.exit(0)
        except Exception:
            pass

    return url


def is_frontmost_app_discord():
    return b"Discord.app" in subprocess.check_output(
        ["osascript", "-e", "get path to frontmost application"]
    )


if __name__ == "__main__":
    window = sys.argv[1]

    url = get_safari_url(window=int(window))
    url = normalise_url(url)

    # I never want to paste Twitter links into Discord; I want fxtwitter
    # so I get the nice link previews.
    if url.startswith("https://twitter.com/") and is_frontmost_app_discord():
        url = url.replace("https://twitter.com/", "https://fxtwitter.com/")

    print(url, end="")
