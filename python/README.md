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
    {
        "name": "pip_compile (--upgrade)",
        "description": "Compile any `requirements.in` files into a list of exact versions in `requirements.txt`.",
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

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/python/pip_compile">
      <code>pip_compile (--upgrade)</code>
    </a>
  </dt>
  <dd>
    Compile any `requirements.in` files into a list of exact versions in `requirements.txt`.
  </dd>
</dl>
<!-- [[[end]]] (checksum: 3e15017c8de1c144defe8f18a08d38b1) -->
