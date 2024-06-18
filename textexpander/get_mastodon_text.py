#!/usr/bin/env python3
"""
Look at the Mastodon URL in the frontmost Safari window, and print it
as a blockquote.
"""

import datetime
import html
import os
import pathlib
import re
import subprocess

import httpx
import hyperlink


ATTACHMENTS_DIR = pathlib.Path.home() / "textfiles" / "Attachments" / "mastodon"


def download(url):
    """
    Download a file to the attachments directory, or do nothing if it's
    already downloaded.
    """
    resp = httpx.get(url)
    content = resp.content

    ATTACHMENTS_DIR.mkdir(exist_ok=True)

    out_path = ATTACHMENTS_DIR / os.path.basename(url)

    try:
        with open(out_path, "xb") as out_file:
            out_file.write(content)
    except FileExistsError:
        if open(out_path, "rb").read() == content:
            pass
        else:
            raise


def normalise_text(text: str) -> str:
    text = text.replace("</p><p>", "\n\n")
    text = text.replace("<p>", "").replace("</p>", "")
    text = text.replace("*", "\\*")
    text = re.sub(
        r'<a href="[^"]+" class="mention hashtag" rel="tag">#<span>(?P<hashtag>[^<]+)</span></a>',
        r"\\#\g<hashtag>",
        text,
    )
    text = re.sub(
        r'<a href="(?P<url>[^"]+)" rel="nofollow noopener noreferrer" translate="no" target="_blank"><span class="invisible">[^<]+</span><span class="ellipsis">[^<]+</span><span class="invisible">[^<]+</span></a>',
        r"\g<url>",
        text,
    )
    text = html.unescape(text)
    return text


if __name__ == "__main__":
    url = subprocess.check_output(
        ["osascript", "-e", 'tell application "Safari" to get URL of document 1']
    ).decode("utf8")

    u = hyperlink.URL.from_text(url)

    # e.g. https://hachyderm.io/@djnavarro/111535929722933178
    # ~>  https://hachyderm.io/api/v1/statuses/111535929722933178
    api_url = f"https://{u.host}/api/v1/statuses/{u.path[1]}".strip()

    resp = httpx.get(api_url)

    post_data = resp.json()

    for attachment in post_data["media_attachments"]:
        download(attachment["url"])

    author = post_data["account"]["display_name"]
    post_url = post_data["url"]

    # e.g. 2023-12-06T22:53:44.536Z
    created_at = datetime.datetime.strptime(
        post_data["created_at"], "%Y-%m-%dT%H:%M:%S.%fz"
    )

    print(f'[{author}]({post_url}) ({created_at.strftime("%-d %B %Y")}):')
    print("")
    for line in normalise_text(post_data["content"]).splitlines():
        print(f"> {line}".strip())

    if post_data["media_attachments"]:
        print(">\n> ", end="")
        for attachment in post_data["media_attachments"]:
            print("![[%s|200]]" % os.path.basename(attachment["url"]), end="")

    print("")
