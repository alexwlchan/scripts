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
        "usage": "deploy_to_pypi",
        "description": """
        deploy a new version of a Python library: bump the version, tag the Git commit, push to PyPI and GitHub.
        """,
    },
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
    <a href="https://github.com/alexwlchan/scripts/blob/main/python/deploy_to_pypi">
      <code>deploy_to_pypi</code>
    </a>
  </dt>
  <dd>
    deploy a new version of a Python library: bump the version, tag the Git commit, push to PyPI and GitHub.
  </dd>

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
<!-- [[[end]]] (checksum: a41fde5ae0ac650aa914107e692982ff) -->
