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
import hyperlink

from urls import get_safari_url


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

    # username = soup.find("div", attrs={"data-testid": "User-Name"}).text.replace(f'@{handle}', '').strip()

    text = soup.find("div", attrs={"data-testid": "tweetText"}).text
    text = text.replace("#", "\\#")

    time = datetime.datetime.fromisoformat(soup.find("time").attrs["datetime"])

    print(f'{url} ({time.strftime("%-d %b %Y")}):')
    print("")
    print(textwrap.indent(text, prefix="> ", predicate=lambda line: True))
