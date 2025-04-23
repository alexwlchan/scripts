# fish_functions

This is a collection of functions for the Fish shell, which are [automatically loaded][functions].
When I call one of these functions for the first time, Fish looks for the corresponding file in this folder and loads the function from there.

[functions]: https://fishshell.com/docs/current/language.html#autoloading-functions

<!-- [[[cog

# This adds the root of the repo to the PATH, which has cog_helpers.py
from os.path import abspath, basename, dirname
import sys

sys.path.append(abspath(dirname(dirname("."))))

import glob
import shlex

import cog

import cog_helpers

folder_name = "fish_functions"

functions = []

for f in sorted(glob.glob("fish_functions/*.fish")):

    # Look for the line in the file that defines the function.
    #
    # e.g. if the file is called 'tmpdir.fish', look for the line that
    # starts 'function tmpdir'
    function_name = basename(f).replace('.fish', '')
    definition_line = next(
        line
        for line in open(f)
        if line.startswith(f'function {function_name}')
    )

    # Now split the definition line into components
    components = shlex.split(definition_line)
    try:
        description_flag = components.index("--description")
    except ValueError:
        raise ValueError(f"No --description flag for {function_name}")
    description = components[description_flag + 1]

    functions.append({"name": basename(f), "description": description})

cog_helpers.create_description_table(folder_name=folder_name, scripts=functions)
]]] -->
<dl>
  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fish_functions/add_repo_to_path.fish">
      <code>add_repo_to_path.fish</code>
    </a>
  </dt>
  <dd>
    Add a folder in my ~/repos directory to my PATH
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fish_functions/append_to_file_if_not_exists.fish">
      <code>append_to_file_if_not_exists.fish</code>
    </a>
  </dt>
  <dd>
    Append a line to a file, but only if it's not already there
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fish_functions/auto_activate_venv.fish">
      <code>auto_activate_venv.fish</code>
    </a>
  </dt>
  <dd>
    Auto activate/deactivate virtualenv when I change directories
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fish_functions/fish_prompt.fish">
      <code>fish_prompt.fish</code>
    </a>
  </dt>
  <dd>
    Write out the prompt
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fish_functions/forget_last_command.fish">
      <code>forget_last_command.fish</code>
    </a>
  </dt>
  <dd>
    Remove the last-typed command from my fish history
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fish_functions/github-clone.fish">
      <code>github-clone.fish</code>
    </a>
  </dt>
  <dd>
    Clone a GitHub repository into my ~/repos directory
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fish_functions/pip_sync.fish">
      <code>pip_sync.fish</code>
    </a>
  </dt>
  <dd>
    Make a virtualenv dependencies look like requirements.txt
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fish_functions/pip_upgrade.fish">
      <code>pip_upgrade.fish</code>
    </a>
  </dt>
  <dd>
    Upgrade requirements.txt lock files with uv
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fish_functions/reload_fish_config.fish">
      <code>reload_fish_config.fish</code>
    </a>
  </dt>
  <dd>
    Load the latest version of my fish config
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fish_functions/tmpdir.fish">
      <code>tmpdir.fish</code>
    </a>
  </dt>
  <dd>
    Create and switch into a temporary directory
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fish_functions/venv.fish">
      <code>venv.fish</code>
    </a>
  </dt>
  <dd>
    Create and activate a new virtual environment
  </dd>
</dl>
<!-- [[[end]]] (checksum: b2b37beea55a61207649c299f0858d15) -->