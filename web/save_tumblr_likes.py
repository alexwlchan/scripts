import datetime
import errno
import functools
import json
import os
import pathlib
import shutil
import subprocess
import sys
import textwrap
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup
import httpx
import hyperlink
import keyring
from sqlite_utils import Database
from sqlite_utils.db import NotFoundError
import termcolor


BACKUP_ROOT = pathlib.Path("/Volumes/Media (Sapphire)/backups/tumblr")


def get_liked_posts(blog_identifier: str, days: int):
    """
    Get a list of all my likes from Tumblr.
    """
    client = httpx.Client(
        base_url="https://api.tumblr.com/v2/blog",
        params={"api_key": keyring.get_password("tumblr", "api_key")},
        headers={"User-Agent": "Alex Chan's personal scripts; alex@alexwlchan.net"},
    )

    params = {}

    while True:
        resp = client.get(f"{blog_identifier}/likes", params=params)
        resp.raise_for_status()

        # If we've gone further back than we need, then we should stop --
        # we don't need to download all of Tumblr, forever.
        if "before" in params:
            before = datetime.datetime.fromtimestamp(int(params["before"]))

            if (datetime.datetime.now() - before).days > days:
                break

        # Note: this can throw a 403 Forbidden error if the list of likes
        # isn't public.  You can get the list of likes if it's private
        # using OAuth, but that's a lot of extra hassle and I cba.
        try:
            posts = resp.json()["response"]["liked_posts"]
        except TypeError:
            print(json.dumps(resp.json(), indent=2, sort_keys=True))
            raise
        yield from posts

        # An empty posts list tells us we've finished.
        if not posts:
            break

        # Tumblr helpfully includes some query parameters in the response that
        # we can use to build our next request.
        params.update(resp.json()["response"]["_links"]["next"]["query_params"])


def log_result(format_template):
    def decorator(inner_fn):
        @functools.wraps(inner_fn)
        def wrapper(**kwargs):
            description = format_template.format(**kwargs)
            try:
                result = inner_fn(**kwargs)
            except Exception as exc:
                wrapped_error = textwrap.indent(
                    textwrap.fill(str(exc), width=85), prefix=" " * 4
                )
                print(termcolor.colored(f"✘ {description}\n{wrapped_error}", "red"))
                raise
            else:
                print(termcolor.colored(f"✔ {description}", "green"))
                return result

        return wrapper

    return decorator


def get_saved_blog_name(*, post_id: str, blog_name: str, db_path: pathlib.Path) -> str:
    """
    Look up the blog name associated with this post ID.

    It might be the blog name that's currently in use, or it might be that
    we've already saved this post under a different name -- if so, prefer
    the already-saved name.
    """
    db = Database(db_path)

    try:
        return db["tumblr_posts"].get(post_id)["blog_name"]
    except NotFoundError:
        db["tumblr_posts"].insert({"post_id": post_id, "blog_name": blog_name})

        return blog_name


@log_result("{post_url}")
def download_tumblr_post(*, post_url, post_data, download_root):
    blog_name = get_saved_blog_name(
        post_id=post_data["id"],
        blog_name=post_data["blog_name"],
        db_path=download_root / "post_ids.db",
    )

    download_dir = (
        download_root / blog_name[0].lower() / blog_name / str(post_data["id"])
    )
    download_dir.mkdir(exist_ok=True, parents=True)

    try:
        with open(download_dir / "info.json", "x") as out_file:
            out_file.write(json.dumps(post_data, indent=2, sort_keys=True))
    except FileExistsError:
        pass

    # Track the assets that we've tried to download previously and failed.
    # If something has failed in the past, don't try to redownload it.
    # This avoids making lots of unnecessary network requests.
    missing_assets = download_root / "missing_assets.txt"
    try:
        known_missing_asset_urls = set([url.strip() for url in open(missing_assets)])
    except FileNotFoundError:
        known_missing_asset_urls = set()

    has_missing_assets = False

    for asset_url in get_asset_urls(post_data):
        if asset_url in known_missing_asset_urls:
            has_missing_assets = True
            continue

        try:
            download_asset_url(
                post_data=post_data, url=asset_url, download_dir=download_dir
            )
        except CannotDownloadAsset:
            has_missing_assets = True
            with open(missing_assets, "a") as out_file:
                out_file.write(asset_url + "\n")

    if has_missing_assets:
        raise CannotDownloadAsset("Could not download all assets")

    return download_dir


def get_asset_urls(post_data):
    """
    Given a blob of metadata about a Tumblr post, get all the asset URLs.
    """
    if post_data["type"] == "photo":
        for photo in post_data["photos"]:
            yield photo["original_size"]["url"]

    elif post_data["type"] in ("answer", "chat", "link", "quote", "text"):
        return

    elif post_data["type"] == "video":
        post_id = post_data["id"]
        players = [p for p in post_data["player"] if p["embed_code"]]

        if post_data["video_type"] == "tumblr":
            yield post_data["video_url"]

        elif post_data["video_type"] == "youtube":
            if all(not p["embed_code"] for p in post_data["player"]):
                return

            try:
                if post_data["source_url"].startswith("https://www.youtube.com/embed"):
                    source_url = post_data["source_url"]
                else:
                    source_url = parse_qs(urlparse(post_data["source_url"]).query)["z"][
                        0
                    ]
            except KeyError:
                best_player = max(players, key=lambda p: p["width"])
                soup = BeautifulSoup(best_player["embed_code"], "html.parser")
                iframe_matches = soup.find_all("iframe", attrs={"id": "youtube_iframe"})
                assert len(iframe_matches) == 1

                source_url = iframe_matches[0].attrs["src"]

            yield source_url

        elif post_data["video_type"] == "vimeo":
            best_player = max(players, key=lambda p: p["width"])
            soup = BeautifulSoup(best_player["embed_code"], "html.parser")
            iframe_matches = soup.find_all("iframe")
            assert len(iframe_matches) == 1

            embed_url = iframe_matches[0].attrs["src"]
            yield embed_url

        elif post_data["video_type"] == "unknown" and post_data.get(
            "source_url", ""
        ).startswith("https://t.umblr.com/redirect?z=http%3A%2F%2Fwww.youtube.com"):
            source_url = parse_qs(urlparse(post_data["source_url"]).query)["z"][0]
            yield source_url

        elif post_data["video_type"] in ("instagram", "vine"):
            # Normally there's a link to Instagram videos in the "permalink_url"
            # field, but sometimes this is missing.  I think it happens when the
            # Instagram video is taken down, and it's no longer viewable on Tumblr.
            # e.g. http://his-shining-tears.tumblr.com/post/146498996350
            try:
                source_url = post_data["permalink_url"]
            except KeyError:
                print(f"Unable to get video URL for {post_id!r}", file=sys.stderr)
            else:
                yield source_url

        elif post_data["video_type"] == "flickr":
            source_url = parse_qs(urlparse(post_data["source_url"]).query)["z"][0]
            print(
                f"Unable to download video for {post_id!r}: {source_url}",
                file=sys.stderr,
            )

        else:
            print(
                f"Unable to download video for {post_id!r}; unrecognised video type {post_data['video_type']!r}",
                file=sys.stderr,
            )

    elif post_data["type"] == "audio":
        # Exammple contents of the "player" field:
        #
        #     <iframe
        #       class="tumblr_audio_player tumblr_audio_player_76004518890"
        #       src="http://example.tumblr.com/post/1234/audio_player_iframe/example/tumblr_1234?audio_file=https%3A%2F%2Fwww.tumblr.com%2Faudio_file%2Fexample%2F1234%2Ftumblr_1234"
        #       frameborder="0"
        #       allowtransparency="true"
        #       scrolling="no"
        #       width="540"
        #       height="169"></iframe>
        #
        if post_data["audio_type"] == "tumblr":
            player_soup = BeautifulSoup(post_data["player"], "html.parser")
            player_matches = player_soup.find_all(
                "iframe", attrs={"class": "tumblr_audio_player"}
            )
            assert len(player_matches) == 1

            src_url = player_matches[0]["src"]
            query_string = parse_qs(urlparse(src_url).query)
            assert len(query_string["audio_file"]) == 1
            audio_file = query_string["audio_file"][0]
            yield audio_file

        elif post_data["audio_type"] == "spotify":
            source_url = post_data["audio_source_url"]
            print(
                f"Unable to download audio file for {post_id!r}: {source_url!r}",
                file=sys.stderr,
            )

        elif post_data["audio_type"] == "soundcloud":
            source_url = post_data["audio_source_url"]
            print(
                f"Unable to download audio file for {post_id!r}: {source_url!r}",
                file=sys.stderr,
            )

        else:
            print(f"Unable to download audio for {post_id!r}", file=sys.stderr)

    else:
        post_type = post_data["type"]
        raise ValueError(f"Unrecognised post type: {post_id!r} ({post_type})")


def download_asset_url(url, *, post_data, download_dir):
    parsed_url = hyperlink.URL.from_text(url)

    if parsed_url.host.endswith(".tumblr.com"):
        out_path = download_dir / parsed_url.path[-1]

        if out_path.exists():
            return

        tmp_path = str(out_path) + ".tmp"

        r = httpx.get(url)

        with open(tmp_path, "wb") as tmp_file:
            tmp_file.write(r.content)

        try:
            os.rename(tmp_path, out_path)
        except OSError as err:
            if err.errno == errno.EXDEV:
                shutil.move(tmp_path, out_path)
            else:
                raise

        return out_path

    elif (
        ("youtube.com" in parsed_url.host)
        or ("vimeo.com" in parsed_url.host)
        or ("instagram.com" in parsed_url.host)
    ):
        # Check if the video (or a video with a similar-looking name) has already
        # been downloaded before trying to download it again.
        if "youtube.com" in parsed_url.host:
            try:
                video_id = parsed_url.get("v")[0]
            except IndexError:
                # e.g. https://www.youtube.com/embed/A7-1KknnAak
                if "embed" in parsed_url.path:
                    video_id = parsed_url.path[-1]
                else:
                    raise CannotDownloadAsset(f"Cannot find video ID: {url}")
        elif ("vimeo.com" in parsed_url.host) or ("instagram.com") in parsed_url.host:
            try:
                video_id = parsed_url.path[-1]
            except IndexError:
                raise CannotDownloadAsset(f"Cannot find video ID: {url}")
        else:
            raise ValueError(f"Cannot find video ID: {url}")

        if any(
            f.endswith((".mp4", ".mkv", ".webm")) and (video_id in f)
            for f in os.listdir(download_dir)
        ):
            return

        try:
            subprocess.check_call(["yt-dlp", url], cwd=download_dir)
            return
        except subprocess.CalledProcessError:
            raise CannotDownloadAsset()

    assert 0, url


class CannotDownloadAsset(Exception):
    pass


if __name__ == "__main__":
    for post_data in get_liked_posts(blog_identifier="alexwlchan.tumblr.com", days=120):
        download_tumblr_post(
            post_url=post_data["post_url"],
            post_data=post_data,
            download_root=pathlib.Path(BACKUP_ROOT),
        )
