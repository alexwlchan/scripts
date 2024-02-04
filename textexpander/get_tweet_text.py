#!/usr/bin/env python3
"""
Look at the tweet in the frontmost Safari window, and print it
as a blockquote suitable for pasting into Obsidian.
"""

import datetime
import regex
import subprocess
import sys
import textwrap

import bs4
import httpx
import hyperlink

from urls import get_safari_url


def get_tco_redirect(url: str) -> str:
    resp = httpx.head(url)
    return resp.headers["location"]


if __name__ == "__main__":
    url = get_safari_url()

    if not hyperlink.DecodedURL.from_text(url).host == "twitter.com":
        sys.exit(f"Not a Twitter URL: {url}")

    handle = hyperlink.DecodedURL.from_text(url).path[0]

    cmd = """
    tell application "Safari"
        tell document 1
            get (do JavaScript "document.querySelector('article').innerHTML")
        end tell
    end tell
    """

    html = subprocess.check_output(["osascript", "-e", cmd]).decode("utf8")

    # Twemoji will be something like <img alt="🌮" …, so go ahead and
    # replace them with native emoji ASAP.
    html = regex.sub(r'<img alt="(\p{Extended_Pictographic})"[^>]+>', r"\g<1>", html)

    soup = bs4.BeautifulSoup(html, "html.parser")

    text = soup.find("div", attrs={"data-testid": "tweetText"}).text
    text = text.replace("#", "\\#")
    text = text.replace("[", "\\[")

    # Look for a link to an external web page
    card = soup.find("div", attrs={"data-testid": "card.wrapper"})

    if card is not None:
        linked_url = card.find("a").attrs["href"]
        text += "\n\n" + get_tco_redirect(linked_url)

    time = datetime.datetime.fromisoformat(soup.find("time").attrs["datetime"])

    print(f'{url} ({time.strftime("%-d %b %Y")}):')
    print("")
    print(textwrap.indent(text, prefix="> ", predicate=lambda line: True))
