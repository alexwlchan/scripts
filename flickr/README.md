# flickr

These scripts do stuff with the Flickr API.

Some scripts that used to be in this folder have moved to [a standalone repo](https://github.com/Flickr-Foundation/flapi.sh).

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
    {
        "usage": "ts",
        "description": """
        run <strong>t</strong>est<strong>s</strong> in a Flickr Foundation Python project (including linting, autoformatting, pytest tests)
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

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/flickr/ts">
      <code>ts</code>
    </a>
  </dt>
  <dd>
    run <strong>t</strong>est<strong>s</strong> in a Flickr Foundation Python project (including linting, autoformatting, pytest tests)
  </dd>
</dl>
<!-- [[[end]]] (checksum: 6f1984b029c50abbbd12d74d6f1b07bb) -->
