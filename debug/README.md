# debug

This is a collection of scripts that use [ANSI escape codes](https://stackoverflow.com/a/5947802/1558022) to print coloured messages to the terminal.

I have them saved as individual shell scripts so I can call them from any of my other scripts.

## The individual scripts

<!-- [[[cog

# This adds the root of the repo to the PATH, which has cog_helpers.py
from os.path import abspath, dirname
import sys

sys.path.append(abspath(dirname(dirname("."))))

import cog_helpers

folder_name = "debug"

scripts = [
    {
        "usage": "print_error [MESSAGE]",
        "description": """
        print an error message in red and to stdout
        """
    },
    {
        "usage": "print_info [MESSAGE]",
        "description": """
        print an info message in blue
        """
    },
    {
        "usage": "print_success [MESSAGE]",
        "description": """
        print a success message in green
        """
    },
    {
        "usage": "print_warning [MESSAGE]",
        "description": """
        print a warning message in yellow
        """
    },
]

cog_helpers.create_description_table(folder_name=folder_name, scripts=scripts)

]]]-->
<dl>
  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/debug/print_error">
      <code>print_error [MESSAGE]</code>
    </a>
  </dt>
  <dd>
    print an error message in red and to stdout
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/debug/print_info">
      <code>print_info [MESSAGE]</code>
    </a>
  </dt>
  <dd>
    print an info message in blue
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/debug/print_success">
      <code>print_success [MESSAGE]</code>
    </a>
  </dt>
  <dd>
    print a success message in green
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/debug/print_warning">
      <code>print_warning [MESSAGE]</code>
    </a>
  </dt>
  <dd>
    print a warning message in yellow
  </dd>
</dl>
<!-- [[[end]]] (sum: b8iS/LTHw2) -->
