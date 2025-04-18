# python

These scripts are all for working with Python.

## The individual scripts

<!-- [[[cog

# This adds the root of the repo to the PATH, which has cog_helpers.py
from os.path import abspath, dirname
import sys

sys.path.append(abspath(dirname(dirname("."))))

import cog_helpers

folder_name = "python"

scripts = [
    {
        "name": "pyfmt [...PATH]",
        "description": "Format Python files with ruff.",
    },
]

cog_helpers.create_description_table(folder_name=folder_name, scripts=scripts)

]]]-->
<dl>
  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/python/pyfmt">
      <code>pyfmt [...PATH]</code>
    </a>
  </dt>
  <dd>
    Format Python files with ruff.
  </dd>
</dl>
<!-- [[[end]]] (checksum: 4c51b7cdb9a034e48bee58b82c75d99c) -->
