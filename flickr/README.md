# flickr

These scripts do stuff with the Flickr API.

## The individual scripts

<!-- [[[cog

# This adds the root of the repo to the PATH, which has cog_helpers.py
from os.path import abspath, dirname
import sys

sys.path.append(abspath(dirname(dirname("."))))

import cog_helpers

folder_name = "flickr"

scripts = [
    {
        "usage": "flapi.sh [METHOD] [PARAMS]",
        "description": """
        call a method with the Flickr API and print the XML response to stdout.
        """,
    },
    {
        "usage": "flphoto.sh [PHOTO_ID]",
        "description": """
        look up a single photo with the Flickr API and print the XML response to stdout.
        """,
    },
    {
        "usage": "fluser_lookup.py [USER_ID]",
        "description": """
        Look up a Flickr user by URL or path alias.
        """,
    },
]

cog_helpers.create_description_table(folder_name=folder_name, scripts=scripts)

]]]-->
<dl>
  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/flickr/flapi.sh">
      <code>flapi.sh [METHOD] [PARAMS]</code>
    </a>
  </dt>
  <dd>
    call a method with the Flickr API and print the XML response to stdout.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/flickr/flphoto.sh">
      <code>flphoto.sh [PHOTO_ID]</code>
    </a>
  </dt>
  <dd>
    look up a single photo with the Flickr API and print the XML response to stdout.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/flickr/fluser_lookup.py">
      <code>fluser_lookup.py [USER_ID]</code>
    </a>
  </dt>
  <dd>
    Look up a Flickr user by URL or path alias.
  </dd>
</dl>
<!-- [[[end]]] (checksum: 37fb345f2f059bad0669a7c8411516b9) -->
