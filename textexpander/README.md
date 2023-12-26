# textexpander

These scripts I invoke as text expansion macros in [TextExpander](https://textexpander.com/).

## The individual scripts

<!-- [[[cog

# This adds the root of the repo to the PATH, which has cog_helpers.py
from os.path import abspath, dirname
import sys

sys.path.append(abspath(dirname(dirname("."))))

import cog_helpers

folder_name = "textexpander"

scripts = [
    {
        "name": "get_mastodon_text.py",
        "description": """
        print a Markdown-formatted blockquote of a Mastodon I've got open in Safari, suitable for pasting into Obsidian
        """,
    },
    {
        "name": "get_safari_url.py",
        "description": """
        print the URL in my frontmost Safari window.
        This makes a couple of tweaks to tidy up the URL, e.g. remove tracking parameters and tidy up some Jekyll stuff for my personal site.
        """,
    },
]

cog_helpers.create_description_table(folder_name=folder_name, scripts=scripts)

]]]-->
<dl>
  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/textexpander/get_mastodon_text.py">
      <code>get_mastodon_text.py</code>
    </a>
  </dt>
  <dd>
    print a Markdown-formatted blockquote of a Mastodon I've got open in Safari, suitable for pasting into Obsidian
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/textexpander/get_safari_url.py">
      <code>get_safari_url.py</code>
    </a>
  </dt>
  <dd>
    print the URL in my frontmost Safari window.
    This makes a couple of tweaks to tidy up the URL, e.g. remove tracking parameters and tidy up some Jekyll stuff for my personal site.
  </dd>
</dl>
<!-- [[[end]]] (checksum: 92cb9f2e13db3a692bf3b95b32c5c773) -->
