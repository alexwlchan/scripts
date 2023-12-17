#!/usr/bin/env python3

import datetime
import os
import re
import sys

import httpx
import termcolor


# A regex to find links to somebody's Twitter profile
#
# e.g. (https://twitter.com/BooksandChokers)
PROFILE_URL_RE = re.compile(r"\(https://twitter\.com/(?P<username>[^\)^/]+)\)")


def fix_emoji(text: str) -> str:
    """
    Replace any Twemoji in the text with the actual emoji characters.
    """
    # A regex to find emoji characters which have been replaced with twimg's
    #
    # e.g. ![✍🏻](https://abs-0.twimg.com/emoji/v2/svg/270d-1f3fb.svg)
    # e.g. ![📚](https://abs-0.twimg.com/emoji/v2/svg/1f4da.svg "Books")
    emoji_twimg_re = re.compile(
        r"!\[(?P<emoji>[^\]]+)\]"
        r'\(https://abs\-0\.twimg\.com/emoji/v2/svg/[0-9a-f\-]+\.svg(?: "[A-Za-z]+")?\)'
    )

    return emoji_twimg_re.sub(repl=r"\g<emoji>", string=text)


def fix_hashtags(text: str) -> str:
    """
    Replace any hashtag links in the text with literal text.
    """
    # A regex to find hashtag links
    #
    # e.g. [#akindofspark](https://twitter.com/hashtag/akindofspark?src=hashtag_click)
    hashtag_re = re.compile(
        r"\[#(?P<hashtag>[a-zA-Z][a-zA-Z0-9]+)\]"
        r"\(https://twitter\.com/hashtag/[a-zA-Z][a-zA-Z0-9]+\?src=hashtag_click\)"
    )

    return hashtag_re.sub(repl=r"\\#\g<hashtag>", string=text)


def get_profile_photo_re(handle: str) -> re.Pattern:
    # A regex to find links to somebody's profile that uses their profile
    # picture in the body of the link, e.g.
    #
    #     [
    #
    #     ![](https://pbs.twimg.com/profile_images/1234/bKbnzots_x96.jpg)
    #
    #     ](https://twitter.com/BooksandChokers)
    #
    return re.compile(
        r"\[\n"
        r"\n"
        r"!\[\]\(https://pbs\.twimg\.com/profile_images/[0-9]+/[a-zA-Z0-9_\.]+\)\n"
        r"\n"
        r"\]\(https://twitter\.com/" + handle + r"\)\n"
    )


def remove_profile_links(text: str, /, *, handle: str) -> str:
    # Remove any profile links that are on a single line, e.g.
    #
    # [Elle McNicoll ✍🏻📚](https://twitter.com/BooksandChokers)
    text = re.sub(
        r"\[[^\]]+\]\(https://twitter\.com/" + handle + r"\)" + "\xa0\n",
        repl="",
        string=text,
    )

    # Remove any profile links that are spread across multiple lines, e.g.
    #
    # [
    #
    # @BooksandChokers
    #
    # ](https://twitter.com/BooksandChokers)
    #
    # .
    text = re.sub(
        r"\[\n\n@"
        + handle
        + r"\n\n\]\(https://twitter\.com/"
        + handle
        + r"\)\n\n(?:·\n)?",
        repl="",
        string=text,
    )

    return text


def remove_individual_tweet_links(text: str, /, *, handle: str) -> str:
    # Remove any links to individual tweets in the thread,
    #
    # e.g. [10 Jun](https://twitter.com/BooksandChokers/status/1667617023801839616)
    return re.sub(
        r"\[[0-9]+ [A-Z][a-z]+\]"
        r"\(https://twitter\.com/" + handle + r"/status/[0-9]+\)\n",
        repl="",
        string=text,
    )


def download_images(text: str, /, *, handle: str) -> str:
    # Download images and save them to Obsidian

    image_match = re.compile(
        r"!\[(?P<alt_text>[^\]]*)\]"
        r"\((?P<url>https://pbs\.twimg\.com/media/(?P<media_id>[a-zA-Z0-9]+)\?format=(?P<format>jpg))\&name=(?P<size>small|medium)\)"
    )

    for m in image_match.finditer(text):
        url = m.group("url")
        out_name = m.group("media_id") + "." + m.group("format")
        out_path = os.path.join(
            os.environ["HOME"],
            "textfiles",
            "Attachments",
            str(datetime.datetime.now().year),
            out_name,
        )

        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        resp = httpx.get(url)
        resp.raise_for_status()

        with open(out_path, "xb") as f:
            f.write(resp.content)

        alt_text = m.group("alt_text")

        if alt_text != "Image":
            text = text.replace(m.group(0), f"![[{out_name}|{alt_text}]]")
        else:
            text = text.replace(m.group(0), f"![[{out_name}]]")

    # Remove the lingering bits from the image link
    text = text.replace("[\n", "")
    text = re.sub(
        r"\]\(https://twitter\.com/" + handle + r"/status/[0-9]+/photo/[0-9]\)\n",
        repl="",
        string=text,
    )

    return text


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <PATH>")

    new_lines = []
    last_line = None

    with open(path) as in_file:
        text = in_file.read()

    handle = re.search(PROFILE_URL_RE, text).group("username")
    print("Detected handle as", termcolor.colored(handle, "blue"))

    profile_photo_re = get_profile_photo_re(handle)
    text = profile_photo_re.sub(repl="", string=text)

    text = fix_emoji(text)
    text = fix_hashtags(text)
    text = remove_profile_links(text, handle=handle)
    text = remove_individual_tweet_links(text, handle=handle)
    text = download_images(text, handle=handle)
    text = re.sub("\n\n", "\n", text)

    with open(path, "w") as out_file:
        out_file.write(text)
