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
        "name": "get_phaenna_ip",
        "description": """
        Get the IP address of Phaenna (my home desktop) within my Tailscale network.
        """
    },
    {
        "name": "imdown",
        "description": """
        I run this when my Internet connection goes down, and it makes an audible "ping" when it comes back up.
        """
    },
    {
        "usage": "rcurl [URL]",
        "description": """
        call curl with a couple of flags that allow it to do resumable downloads, which is useful for large files.
        """
    },
    {
        "usage": "save_instagram_post URL",
        "description": """
        save the photos from a single Instagram post to a temporary directory
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
    <a href="https://github.com/alexwlchan/scripts/blob/main/web/get_phaenna_ip">
      <code>get_phaenna_ip</code>
    </a>
  </dt>
  <dd>
    Get the IP address of Phaenna (my home desktop) within my Tailscale network.
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
    <a href="https://github.com/alexwlchan/scripts/blob/main/web/rcurl">
      <code>rcurl [URL]</code>
    </a>
  </dt>
  <dd>
    call curl with a couple of flags that allow it to do resumable downloads, which is useful for large files.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/web/save_instagram_post">
      <code>save_instagram_post URL</code>
    </a>
  </dt>
  <dd>
    save the photos from a single Instagram post to a temporary directory
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
<!-- [[[end]]] (checksum: 12930590ef863d6c23f93554fb170cd5) -->
