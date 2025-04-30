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
        "name": "pip_compile (--upgrade) (--no-cache)",
        "description": "Compile any `requirements.in` files into a list of exact versions in `requirements.txt`.",
    },
    {
        "name": "run_pip_sync (--no-cache)",
        "description": "A wrapper around `uv pip sync`. You don't need to call this directly.",
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
      <code>pip_compile (--upgrade) (--no-cache)</code>
    </a>
  </dt>
  <dd>
    Compile any `requirements.in` files into a list of exact versions in `requirements.txt`.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/python/run_pip_sync">
      <code>run_pip_sync (--no-cache)</code>
    </a>
  </dt>
  <dd>
    A wrapper around `uv pip sync`. You don't need to call this directly.
  </dd>
</dl>
<!-- [[[end]]] (checksum: bc5aac2674e0836cb28c25fa59413628) -->
