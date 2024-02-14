#!/usr/bin/env python3

import contextlib
import datetime
import json
import os
import pathlib
import shutil
import subprocess
import tarfile
import tempfile

import bs4
import httpx
import keyring


BACKUP_ROOT = pathlib.Path("/Volumes/Media (Sapphire)/backups/pinboard")


def write_to_file(name: str, contents: str) -> None:
    """
    Write a string to a text file, and log that you're doing it.
    """
    path = BACKUP_ROOT / name
    print(f"    ~> {path}")
    path.write_text(contents)


def get_bookmarks_json(username: str, password: str) -> str:
    """
    Call the Pinboard API to get a complete list of my bookmarks.

    Return the result as a pretty-printed JSON string.
    """
    resp = httpx.get(
        "https://api.pinboard.in/v1/posts/all",
        params={"format": "json"},
        auth=(username, password),
    )

    resp.raise_for_status()

    json_string = json.dumps(resp.json(), indent=2, sort_keys=True)

    return json_string


def get_cache_ids(username: str, password: str) -> dict[str, str]:
    """
    Get a list of cache IDs for bookmarks in my account.

    These are the URLs where Pinboard takes archived snapshots of
    web pages, e.g. https://pinboard.in/cached/1234567890/

    Returns a dict (bookmarked URL) -> (cache ID).
    """
    # Start by logging in to Pinbaord, so we have the appropriate
    # cookies in our session.
    client = httpx.Client(follow_redirects=True)

    resp = client.post(
        "https://pinboard.in/auth/", data={"username": username, "password": password}
    )
    resp.raise_for_status()

    # Now start fetching cache IDs from my account.
    cache_ids: dict[str, str] = {}

    url = f"https://pinboard.in/u:{username}"

    while True:
        print(f"    ... fetching cache IDs from {url}")
        resp = client.get(url, params={"per_page": "160"})
        resp.raise_for_status()

        soup = bs4.BeautifulSoup(resp.text, "html.parser")

        # The structure of the page is of the form:
        #
        #     <div id="bookmarks">
        #       <div class="bookmark">
        #         <a class="bookmark_title" href="http://example.net">Example</a>
        #         <a class="cached" href="/cached/1234567890/">☑</a>
        #         …
        #
        bookmarks_div = soup.find("div", attrs={"id": "bookmarks"})
        bookmarks = bookmarks_div.find_all("div", attrs={"class": "bookmark"})

        for b in bookmarks:
            href = b.find("a", attrs={"class": "bookmark_title"}).attrs["href"]
            cache_link = b.find("a", attrs={"class": "cached"})

            if cache_link is None:
                continue

            this_cache_id = cache_link.attrs["href"].split("/")[-2]

            cache_ids[href] = this_cache_id

        # The pagination link, if present, will be something like:
        #
        #      <a class="next_prev" href="/u:alexwlchan/before:1234">« earlier</a>
        #
        pagination_link = soup.find("a", attrs={"class": "next_prev"})

        if "earlier" not in pagination_link.text:
            break

        url = "https://pinboard.in" + pagination_link.attrs["href"]

    return cache_ids


def wget(*args):
    subprocess.call(["wget"] + list(args), stdout=subprocess.DEVNULL)


@contextlib.contextmanager
def wget_context(username: str, password: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)

        wget(
            "--save-cookies",
            "pinboard-cookies.txt",
            "--keep-session-cookies",
            "--delete-after",
            "--output-file",
            "-",
            "--post-data",
            f"username={username}&password={password}",
            "https://pinboard.in/auth/",
        )

        yield

        os.unlink("pinboard-cookies.txt")


def download_single_archive(url: str, cache_id: str):
    cache_dir = BACKUP_ROOT / "archive" / cache_id[0] / cache_id
    cache_path = cache_dir.with_suffix(".tar.gz")

    # If the archive is already downloaded, there's nothing to do.
    if cache_path.exists():
        return

    print(f"    ... saving https://pinboard.in/cached/{cache_id}/")
    print(f"        {url}")

    # Otherwise, start downloading the archive into a temporary directory.
    # Clear any pending downloads first.
    tmp_dir = cache_dir.with_suffix(".tmp")
    tmp_dir.mkdir(parents=True, exist_ok=True)

    shutil.rmtree(tmp_dir)

    wget(
        "--adjust-extension",
        "--span-hosts",
        "--no-verbose",
        "--convert-links",
        "--page-requisites",
        "--no-directories",
        "-e",
        "robots=off",
        "--load-cookies",
        "pinboard-cookies.txt",
        "--output-file",
        "-",
        "--directory-prefix",
        str(tmp_dir),
        f"https://pinboard.in/cached/{cache_id}/",
    )

    with tarfile.open(cache_path, "w:gz") as tf:
        tf.add(tmp_dir, arcname=cache_id)

    print(f"        {cache_path}")

    shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    username = "alexwlchan"

    password = keyring.get_password("pinboard", "password")
    assert password is not None

    now = datetime.date.today().strftime("%Y-%m-%d")

    print("*** Getting a JSON copy of my bookmarks data")
    json_string = get_bookmarks_json(username, password)

    for name in (f"bookmarks.{now}.json", "bookmarks.json"):
        write_to_file(name, contents=json_string)

    print("")

    print("*** Getting a list of cache IDs")
    all_cache_ids = get_cache_ids(username, password)

    for name in (f"cache_ids.{now}.json", "cache_ids.json"):
        write_to_file(name, contents=json.dumps(all_cache_ids))

    all_cache_ids = json.load(open(BACKUP_ROOT / "cache_ids.json"))

    print("")

    print("*** Saving archive files using wget")

    with wget_context(username, password):
        for url, cache_id in all_cache_ids.items():
            download_single_archive(url, cache_id)
