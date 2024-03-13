#!/usr/bin/env python3
"""
This is a wrapper around yt-dlp that has special behaviour
for YouTube playlists.

When it detects a playlist, it can run up to five downloads in parallel --
this can makes downloads significantly faster.

See https://alexwlchan.net/2020/how-to-do-parallel-downloads-with-youtube-dl/
"""

import os
import subprocess
import sys

import hyperlink


def is_playlist(url: str) -> bool:
    """
    Returns True if a YouTube URL is a playlist, false otherwise.
    """
    u = hyperlink.DecodedURL.from_text(url)
    return bool(u.get("list"))


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

    if "--write-sub" in remaining_args:
        sys.exit("Did you mean --write-subs?")

    # I always want subtitles in srt format, so make sure I've done that.
    #
    # Note: I could add this automatically, but it means vanilla yt-dlp
    # and my wrapper would behave differently.  That could get confusing!
    # So just add a prompt rather than fixing it.
    if (
        "--write-subs" in remaining_args or "--write-auto-subs" in remaining_args
    ) and "--convert-subtitles=srt" not in remaining_args:
        sys.exit("Did you forget to add --convert-subtitles=srt?")

    if len(youtube_url_matches) != 1:
        subprocess.check_call([yt_dlp_path] + argv)
        sys.exit(0)

    youtube_url = youtube_url_matches[0]

    # If this is a YouTube URL but it's not a playlist, then it's probably
    # a single video.  Download it as normal.
    if not is_playlist(youtube_url):
        subprocess.check_call([yt_dlp_path] + argv)

    # Otherwise, this is a playlist, so we want to download it in parallel.
    else:
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
