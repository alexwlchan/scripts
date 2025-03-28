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

import hyperlink


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
    get_ids_proc = subprocess.Popen(
        [yt_dlp_path, "--get-id", youtube_url], stdout=subprocess.PIPE
    )

    subprocess.check_call(
        ["xargs", "-I", "{}", "-P", "5", yt_dlp_path]
        + remaining_args
        + ["https://youtube.com/watch?v={}"],
        stdin=get_ids_proc.stdout,
    )

    get_ids_proc.wait()


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
