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
        "usage": "deploy_to_pypi",
        "description": """
        deploy a new version of a Flickr Foundation Python library: bump the version, tag the Git commit, push to PyPI and GitHub.
        """,
    },
]

cog_helpers.create_description_table(folder_name=folder_name, scripts=scripts)

]]]-->
<dl>
  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/flickr/deploy_to_pypi">
      <code>deploy_to_pypi</code>
    </a>
  </dt>
  <dd>
    deploy a new version of a Flickr Foundation Python library: bump the version, tag the Git commit, push to PyPI and GitHub.
  </dd>
</dl>
<!-- [[[end]]] (checksum: 25a2e0861d7f789ae830f7da3763f089) -->
