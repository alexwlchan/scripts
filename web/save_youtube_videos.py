#!/usr/bin/env python3
"""
Make a local copy of one or more YouTube videos.
"""

import functools
import json
import os
import pathlib
import subprocess
import sys
import textwrap
from typing import Literal

import hyperlink
from sqlite_utils import Database
from sqlite_utils.db import NotFoundError
import termcolor


BACKUP_ROOT = pathlib.Path("/Volumes/Media (Sapphire)/backups/youtube/videos")


def youtube_dl(*args, **kwargs):
    return (
        subprocess.check_output(["yt-dlp"] + list(args), **kwargs)
        .strip()
        .decode("utf8")
    )


def get_video_id(url):
    """
    Given the URL of a YouTube video, return the video ID.
    """
    parsed_url = hyperlink.URL.from_text(url)

    if parsed_url.host != "www.youtube.com":
        raise ValueError(f"Not the URL of a YouTube video: {url!r}")

    video_id = parsed_url.get("v")

    if len(video_id) == 1:
        return video_id[0]
    else:
        raise ValueError(f"Not the URL of a YouTube video: {url!r}")


def get_uploader(*, video_id, db_path):
    db = Database(db_path)

    try:
        return db["youtube_uploaders"].get(video_id)["uploader"]
    except NotFoundError:
        uploader = json.loads(
            youtube_dl("--dump-json", f"https://www.youtube.com/watch?v={video_id}")
        )["uploader"]

        db["youtube_uploaders"].insert(
            {"video_id": video_id, "uploader": uploader}, pk="video_id"
        )

        return uploader


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
                if result == "downloaded":
                    print(termcolor.colored(f"✔ {description}", "green"))
                return result

        return wrapper

    return decorator


def classify_file_type(
    video_id: str, filename: pathlib.Path
) -> Literal["video", "info", "thumbnail", "subtitles"] | None:
    """
    Given an already-downloaded file, work out what sort of file it is.
    """
    if filename.name.endswith(".part"):
        os.unlink(filename)
        return None

    if filename.name.endswith(
        (
            f" [{video_id}].mp4",
            f" [{video_id}].mkv",
            f" [{video_id}].webm",
        )
    ):
        return "video"

    if filename.name.endswith(
        (
            f" [{video_id}].jpg",
            f" [{video_id}].webp",
        )
    ):
        return "thumbnail"

    if filename.name.endswith(f" [{video_id}].info.json"):
        return "info"

    if filename.name.endswith(
        (
            ".vtt",
            f" [{video_id}].live_chat.json",
        )
    ):
        return "subtitles"

    raise ValueError(f"Unrecognised filename: {filename}")


def fix_info_json(path: pathlib.Path) -> None:
    """
    Tidy up the contents of the info.json fie.
    """
    with open(path) as in_file:
        data = json.load(in_file)

    # These are a couple of fields which are very large, don't contain
    # much useful metadata, and point to transient URLs that don't work
    # later.
    for key in (
        "formats",
        "automatic_captions",
        "thumbnails",
        "heatmap",
        "_format_sort_fields",
        "subtitles",
    ):
        if key in data:
            del data[key]

    json_string = json.dumps(data, indent=2)

    with open(path, "w") as out_file:
        out_file.write(json_string)


@log_result("https://youtube.com/watch?v={video_id}")
def download_video(*, video_id, download_root):
    uploader = get_uploader(video_id=video_id, db_path=download_root / "uploaders.db")

    # I save enough videos that saving them all into a single directory is
    # impractical.  Instead, sort videos by the first character of their uploader.
    #
    download_dir = download_root / uploader.lower()[0] / uploader

    download_dir.mkdir(exist_ok=True, parents=True)

    # Look to see if this video has been downloaded before.  If it has, skip any
    # further processing.
    matching_filenames = {
        filename: classify_file_type(video_id, download_dir / filename)
        for filename in os.listdir(download_dir)
        if video_id in filename
    }

    has_video = "video" in matching_filenames.values()
    has_info = "info" in matching_filenames.values()
    has_thumbnail = "thumbnail" in matching_filenames.values()

    if has_video and has_thumbnail and has_info:
        return

    # Construct the command.  The expensive bit is redownloading the
    # video file, so don't do that if it's already downloaded.
    video_url = f"https://youtube.com/watch?v={video_id}"
    cmd = [video_url, "--write-sub"]

    if has_video:
        cmd.append("--skip-download")

    if not has_info:
        cmd.append("--write-info-json")

    if not has_thumbnail:
        cmd.append("--write-thumbnail")

    try:
        youtube_dl(*cmd, cwd=download_dir)
        print(download_dir)

        for f in os.listdir(download_dir):
            if f.endswith(".info.json"):
                fix_info_json(download_dir / f)

        return "downloaded"
    except subprocess.CalledProcessError as err:  # pragma: no cover
        print(f"Unable to download {video_url}: {err}", file=sys.stderr)
        raise


if __name__ == "__main__":
    for url in sys.argv[1:]:
        video_id = get_video_id(url)
        try:
            download_video(video_id=video_id, download_root=BACKUP_ROOT)
        except Exception:
            pass
