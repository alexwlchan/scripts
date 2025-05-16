#!/usr/bin/env python3
"""
This is a wrapper around yt-dlp that has a couple of special behaviours:

*   It does parallel downloads for YouTube playlists, which is must
    faster than vanilla yt-dlp.

*   It enforces a couple of rules around downloading subtitles, to ensure
    I always remember to download them in a consistent way.

The goal is that this is a drop-in replacement for vanilla yt-dlp: if it
downloads something, it downloads the exact same set of files.  You could
copy any command that uses this script onto a machine running the regular
tool and it would work as-is.  It might check extra rules or run faster,
but it should never download something different to the regular tool.
"""

import os
import subprocess
import sys
import time

import hyperlink
import termcolor


def is_youtube_playlist(url: str) -> bool:
    """
    Returns True if a YouTube URL is a playlist, false otherwise.
    """
    u = hyperlink.DecodedURL.from_text(url)
    assert "youtube.com" in u.host
    return bool(u.get("list"))


def download_parallel_playlist(youtube_url: str, remaining_args: list[str]) -> None:
    """
    Download a YouTube playlist in parallel.

    See https://alexwlchan.net/2020/how-to-do-parallel-downloads-with-youtube-dl/
    """
    print(termcolor.colored("-> This is a playlist, downloading in parallel", "blue"))

    get_ids_proc = subprocess.Popen(
        [yt_dlp_path, "--get-id", youtube_url], stdout=subprocess.PIPE
    )

    xargs_proc = subprocess.Popen(
        ["xargs", "-I", "{}", "-P", "5", yt_dlp_path, "--quiet"]
        + remaining_args
        + ["https://youtube.com/watch?v={}"],
        stdin=get_ids_proc.stdout,
    )

    seen_filenames = set()

    while get_ids_proc.returncode is None and xargs_proc.returncode is None:
        get_ids_proc.poll()
        xargs_proc.poll()

        new_filenames = {
            f
            for f in os.listdir(".")
            if f not in seen_filenames and not f.endswith(".part")
        }

        if "-x" in remaining_args:
            new_filenames = {f for f in new_filenames if f.endswith(".mp3")}

        if new_filenames:
            print("\n".join(new_filenames))
            seen_filenames |= new_filenames
            time.sleep(0.05)
        else:
            time.sleep(0.1)

    new_filenames = {
        f
        for f in os.listdir(".")
        if f not in seen_filenames and not f.endswith(".part")
    }
    if new_filenames:
        print("\n".join(new_filenames))


if __name__ == "__main__":
    argv = sys.argv[1:]

    # Where is yt-dlp?
    #
    # sys.executable returns the path to the currently running Python,
    # and we can go from there to get the path to yt-dlp.
    yt_dlp_path = os.path.join(os.path.dirname(sys.executable), "yt-dlp")

    # Look for a YouTube URL in the argument list.  If we don't find one,
    # assume we're downloading some other source and call yt-dlp as usual.
    youtube_url_matches = [a for a in argv if "youtube.com" in a]
    remaining_args = [a for a in argv if "youtube.com" not in a]

    if len(youtube_url_matches) != 1:
        subprocess.check_call([yt_dlp_path] + argv)
        sys.exit(0)

    youtube_url = youtube_url_matches[0]

    if is_youtube_playlist(youtube_url):
        download_parallel_playlist(
            youtube_url=youtube_url, remaining_args=remaining_args
        )
    else:
        subprocess.check_call([yt_dlp_path] + argv)
