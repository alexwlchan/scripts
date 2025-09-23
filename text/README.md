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
        "usage": "fix_whitespace [PATH]",
        "description": """
        when I copy/paste text into Obsidian from th web, this cleans up some of the extraneous whitespace.
        """,
    },
    {
        "usage": "longlines [PATH]",
        "description": "print the line numbers of the longest lines in the file."
    },
    {
        "usage": "midline [PATH]",
        "description": "print the line in the middle of a file, e.g. if the file has 5 lines, it prints line 3"
    },
    {
        "usage": "natsize.py < [NUMBER]",
        "description": "prints a numeric file size as a human-readable string, e.g. `32036032` becomes `32.0 MB`",
    },
    {
        "usage": "noplaylist.py < [URL]",
        "description": "removes the `list` query parameter from a YouTube URL; I use it with `youtube-dl`",
    },
    {
        "usage": "peek < SECRET",
        "description": "show a few characters of a secret, without printing the whole value in plain text"
    },
    {
        "name": "pp_xml.sh < [TEXT]",
        "description": """
        alias for <code>xmllint --format - | pygmentize -l xml</code>, which pretty-prints a blob of XML with coloured syntax highlighting.
        """,
    },
    {
        "name": "r",
        "description": """
        an alias for `rg`, aka <a href="https://geoff.greer.fm/ag/">the Silver Searcher</a>. (Yes, I really am too lazy to type two whole characters.)
        """,
    },
    {
        "usage": "recog",
        "description": """
        Find all the README files under the current folder, and process them using <a href="https://nedbatchelder.com/code/cog">Cog</a>.
        """
    },
    {
        "usage": "reverse < [PATH]",
        "description": "prints the lines of text, but in reverse order.",
    },
    {
        "usage": "smartify.py [PATH]",
        "description": "apply smart typography to a text file."
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
    <a href="https://github.com/alexwlchan/scripts/blob/main/text/fix_whitespace">
      <code>fix_whitespace [PATH]</code>
    </a>
  </dt>
  <dd>
    when I copy/paste text into Obsidian from th web, this cleans up some of the extraneous whitespace.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/text/longlines">
      <code>longlines [PATH]</code>
    </a>
  </dt>
  <dd>
    print the line numbers of the longest lines in the file.
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
    <a href="https://github.com/alexwlchan/scripts/blob/main/text/natsize.py">
      <code>natsize.py < [NUMBER]</code>
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
    <a href="https://github.com/alexwlchan/scripts/blob/main/text/peek">
      <code>peek < SECRET</code>
    </a>
  </dt>
  <dd>
    show a few characters of a secret, without printing the whole value in plain text
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/text/pp_xml.sh">
      <code>pp_xml.sh < [TEXT]</code>
    </a>
  </dt>
  <dd>
    alias for <code>xmllint --format - | pygmentize -l xml</code>, which pretty-prints a blob of XML with coloured syntax highlighting.
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
    <a href="https://github.com/alexwlchan/scripts/blob/main/text/recog">
      <code>recog</code>
    </a>
  </dt>
  <dd>
    Find all the README files under the current folder, and process them using <a href="https://nedbatchelder.com/code/cog">Cog</a>.
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
    <a href="https://github.com/alexwlchan/scripts/blob/main/text/smartify.py">
      <code>smartify.py [PATH]</code>
    </a>
  </dt>
  <dd>
    apply smart typography to a text file.
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
</dl>
<!-- [[[end]]] (sum: FyzA8+tT8Q) -->