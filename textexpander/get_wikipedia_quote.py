#!/usr/bin/python3
"""
Look at the Wikipedia URL in my frontmost browser window, and print
a link with a quote of the first paragraph.
"""

import re

import bs4
import httpx

from urls import get_safari_url


if __name__ == "__main__":
    url = get_safari_url()
    assert "wikipedia.org" in url

    resp = httpx.get(url)

    soup = bs4.BeautifulSoup(resp.text, "html.parser")

    title = soup.find("span", attrs={"class": "mw-page-title-main"}).text
    text = re.sub(
        r"\[\d+\]", "", soup.find("div", attrs={"id": "mw-content-text"}).find("p").text
    )

    print(f"[{title}]({url}):")
    print("")
    print(f"> {text}")
