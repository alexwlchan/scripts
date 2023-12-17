#!/usr/bin/python3

import os
import subprocess
import sys

import httpx


def get_safari_url(window: str) -> str:
    cmd = ["/Users/alexwlchan/.cargo/bin/safari", "url", "--window", window]

    url = subprocess.check_output(cmd).decode("utf8")

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


if __name__ == "__main__":
    window = sys.argv[1]

    print(get_safari_url(window=window), end="")
