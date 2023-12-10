#!/usr/bin/env python3
"""
Look at the Mastodon URL in the frontmost Safari window, and print it
as a blockquote.
"""

import subprocess

import bs4
import httpx


if __name__ == "__main__":
    url = (
        subprocess.check_output(["/usr/local/bin/safari", "url"]).decode("utf8").strip()
    )
    resp = httpx.get(url)
    soup = bs4.BeautifulSoup(resp, "html.parser")

    text = soup.find("meta", attrs={"name": "description"}).attrs["content"]
    author = soup.find("meta", attrs={"property": "og:title"}).attrs["content"]
    url = soup.find("meta", attrs={"property": "og:url"}).attrs["content"]

    print(f"[{author}]({url}):\n")

    for line in text.splitlines():
        print(f"> {line.rstrip()}")
