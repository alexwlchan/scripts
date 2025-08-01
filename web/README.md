# web

These scripts are for interacting with stuff on the web.

## The individual scripts

<!-- [[[cog

# This adds the root of the repo to the PATH, which has cog_helpers.py
from os.path import abspath, dirname
import sys

sys.path.append(abspath(dirname(dirname("."))))

import cog_helpers

folder_name = "web"

scripts = [
    {
        "name": "caddyfmt",
        "description": "Format all of my Caddyfiles, which are config files for my web server."
    },
    {
        "name": "imdown",
        "description": """
        I run this when my Internet connection goes down, and it makes an audible "ping" when it comes back up.
        """
    },
    {
        "name": "scrape_really_useful_boxes.py",
        "description": """
        scrape the Really Useful Boxes product catalogue, so I can search for boxes in ways their website doesn't allow – in particular, by dimensions, so I can find boxes that fit into specific spaces.<br/><br/><img src="really_useful_boxes.png">
        """
    },
    {
        "name": "yt-dlp.py",
        "description": """
        this is a wrapper around <a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a> that does parallel downloads of videos in playlists.
        """
    },
]

cog_helpers.create_description_table(folder_name=folder_name, scripts=scripts)

]]]-->
<dl>
  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/web/caddyfmt">
      <code>caddyfmt</code>
    </a>
  </dt>
  <dd>
    Format all of my Caddyfiles, which are config files for my web server.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/web/imdown">
      <code>imdown</code>
    </a>
  </dt>
  <dd>
    I run this when my Internet connection goes down, and it makes an audible "ping" when it comes back up.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/web/scrape_really_useful_boxes.py">
      <code>scrape_really_useful_boxes.py</code>
    </a>
  </dt>
  <dd>
    scrape the Really Useful Boxes product catalogue, so I can search for boxes in ways their website doesn't allow – in particular, by dimensions, so I can find boxes that fit into specific spaces.<br/><br/><img src="really_useful_boxes.png">
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/web/yt-dlp.py">
      <code>yt-dlp.py</code>
    </a>
  </dt>
  <dd>
    this is a wrapper around <a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a> that does parallel downloads of videos in playlists.
  </dd>
</dl>
<!-- [[[end]]] (sum: vPvQ8JA/hi) -->
