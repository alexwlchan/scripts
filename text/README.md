# text

These are utilities for manipulating streams of text; I consider them in a similar category to Unix staples like <code>head</code> and <code>tail</code>.

## The individual scripts

<!-- [[[cog

# This adds the root of the repo to the PATH, which has cog_helpers.py
from os.path import abspath, dirname
import sys

sys.path.append(abspath(dirname(dirname("."))))

import cog_helpers

folder_name = "text"

scripts = [
    {
        "usage": "body -n [LINENO] [PATH]",
        "description": """
        print the nth line of a file.
        This is meant to fill a gap between the Unix utilities `head` and `tail`.
        """,
    },
    {
        "usage": "fix_twitter_thread.py [PATH]",
        "description": """
        when I copy/paste a Twitter thread into Obsidian, this does some 
        initial tidying up of the formatting for me.
        """,
    },
    {
        "usage": "midline [PATH]",
        "description": "print the line in the middle of a file, e.g. if the file has 5 lines, it prints line 3"
    },
    {
        "usage": "natsize < [NUMBER]",
        "description": "prints a numeric file size as a human-readable string, e.g. `32036032` becomes `32.0 MB`",   
    },
    {
        "usage": "noplaylist.py < [URL]",
        "description": "removes the `list` query parameter from a YouTube URL; I use it with `youtube-dl`",  
    },
    {
        "name": "r",
        "description": """
        an alias for `rg`, aka <a href="https://geoff.greer.fm/ag/">the Silver Searcher</a>. (Yes, I really am too lazy to type two whole characters.)
        """,
    },
    {
        "usage": "randline [NUMBER] < [PATH]",
        "description": "prints randomly selected lines from the given text. If `NUMBER` is unspecified, it prints a single line.",
    },
    {
        "usage": "reverse < [PATH]",
        "description": "prints the lines of text, but in reverse order.",
    },
    {
        "usage": "sumsizes.py < [PATH]",
        "description": """
        prints a human-readable data size for the numbers passed on stdin.

            $ echo -e '100\\n 201287\\n 3190817' | sumsizes
            3.4MB

        """
    },
    {
        "usage": "tally < [PATH]",
        "description": "prints a tally of lines in the given text.",
    },
    {
        "usage": "echo [STRING] | utf8info",
        "description": """
        read UTF-8 on stdin and print out the raw Unicode "
        "codepoints. This is a Docker wrapper around <a href="https://github.com/lunasorcery/utf8info">a tool of the same name</a> by @lunasorcery.
        """,
    },
]

cog_helpers.create_description_table(folder_name=folder_name, scripts=scripts)

]]]-->
<dl>
<dt>
<a href="https://github.com/alexwlchan/scripts/blob/main/text/body">
<code>body -n [LINENO] [PATH]</code>
</a>
</dt>
<dd>
print the nth line of a file.
This is meant to fill a gap between the Unix utilities `head` and `tail`.
</dd>
<dt>
<a href="https://github.com/alexwlchan/scripts/blob/main/text/fix_twitter_thread.py">
<code>fix_twitter_thread.py [PATH]</code>
</a>
</dt>
<dd>
when I copy/paste a Twitter thread into Obsidian, this does some 
initial tidying up of the formatting for me.
</dd>
<dt>
<a href="https://github.com/alexwlchan/scripts/blob/main/text/midline">
<code>midline [PATH]</code>
</a>
</dt>
<dd>
print the line in the middle of a file, e.g. if the file has 5 lines, it prints line 3
</dd>
<dt>
<a href="https://github.com/alexwlchan/scripts/blob/main/text/natsize">
<code>natsize < [NUMBER]</code>
</a>
</dt>
<dd>
prints a numeric file size as a human-readable string, e.g. `32036032` becomes `32.0 MB`
</dd>
<dt>
<a href="https://github.com/alexwlchan/scripts/blob/main/text/noplaylist.py">
<code>noplaylist.py < [URL]</code>
</a>
</dt>
<dd>
removes the `list` query parameter from a YouTube URL; I use it with `youtube-dl`
</dd>
<dt>
<a href="https://github.com/alexwlchan/scripts/blob/main/text/r">
<code>r</code>
</a>
</dt>
<dd>
an alias for `rg`, aka <a href="https://geoff.greer.fm/ag/">the Silver Searcher</a>. (Yes, I really am too lazy to type two whole characters.)
</dd>
<dt>
<a href="https://github.com/alexwlchan/scripts/blob/main/text/randline">
<code>randline [NUMBER] < [PATH]</code>
</a>
</dt>
<dd>
prints randomly selected lines from the given text. If `NUMBER` is unspecified, it prints a single line.
</dd>
<dt>
<a href="https://github.com/alexwlchan/scripts/blob/main/text/reverse">
<code>reverse < [PATH]</code>
</a>
</dt>
<dd>
prints the lines of text, but in reverse order.
</dd>
<dt>
<a href="https://github.com/alexwlchan/scripts/blob/main/text/sumsizes.py">
<code>sumsizes.py < [PATH]</code>
</a>
</dt>
<dd>
prints a human-readable data size for the numbers passed on stdin.

    $ echo -e '100\n 201287\n 3190817' | sumsizes
    3.4MB
</dd>
<dt>
<a href="https://github.com/alexwlchan/scripts/blob/main/text/tally">
<code>tally < [PATH]</code>
</a>
</dt>
<dd>
prints a tally of lines in the given text.
</dd>
<dt>
<a href="https://github.com/alexwlchan/scripts/blob/main/text/echo">
<code>echo [STRING] | utf8info</code>
</a>
</dt>
<dd>
read UTF-8 on stdin and print out the raw Unicode "
"codepoints. This is a Docker wrapper around <a href="https://github.com/lunasorcery/utf8info">a tool of the same name</a> by @lunasorcery.
</dd>
</dl>
<!-- [[[end]]] (checksum: afe7ca0c0f56a356286950da6b8332a3) -->