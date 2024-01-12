#!/usr/bin/env python3
"""
Create a reference-style Markdown link to my frontmost Safari URL.

This assumes I've already typed the link label, and it adds the reference.
It tries to deduce a sensible name for the reference, or prompts for input
if it can't pick one.
"""

import subprocess

import hyperlink

from get_safari_url import normalise_url
from urls import get_safari_url


def get_reference_label(url: str) -> str:
    """
    Get the reference label that should accompany this URL in the link.
    """
    u = hyperlink.DecodedURL.from_text(url)

    # If it's a package on PyPI, the link label is the project name.
    #
    # e.g. "https://pypi.org/project/eyed3/" ~> "eyed3"
    if u.host == "pypi.org" and len(u.path) >= 2 and u.path[0] == "project":
        return u.path[1]

    # If we can't deduce a default link name, prompt the user for input.
    cmd = [
        "osascript",
        "-e",
        f"""
        set theResponse to display dialog "The URL is {url}.\n\nWhat’s the link label?" default answer ""
        get text returned of theResponse
    """,
    ]

    label = subprocess.check_output(cmd).decode("utf8").strip()

    return label


if __name__ == "__main__":
    url = get_safari_url()
    url = normalise_url(url)

    label = get_reference_label(url)

    print(f"[{label}]\n\n[{label}]: {url}")
