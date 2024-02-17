# fs

These are scripts for manipulating files and folders in my local filesystem.

## The individual scripts

<!-- [[[cog

# This adds the root of the repo to the PATH, which has cog_helpers.py
from os.path import abspath, dirname
import sys

sys.path.append(abspath(dirname(dirname("."))))

import cog_helpers

folder_name = "fs"

scripts = [
    {
        "name": "cdir",
        "description": """
        counts all the entries in subfolders under the working directory, and prints them in a table
        <p><pre><code>$ cdir
         37 fishconfig
         48 repros
         51 colossus-wheels
         70 services
        292 .git
        -------
        699</code></pre></p>
        """
    },
    {
        "usage": "deepestdir [ROOT]",
        "description": "prints the directory which is the deepest child of the given directory"
    },
    {
        "name": "emptydir.py",
        "description": "removes any empty directories under the current one (including directories that are empty aside from files that can be safely deleted, e.g. <code>.DS_Store</code>)"
    },
    {
        "name": "flatten",
        "description": """
        flattens a directory structure.
        When you run it in a folder, it moves any files in subfolders into the top-level folders, then deletes the now-empty folder.
        """
    },
    {
        "variants": ["hide [PATH]", "unhide [PATH]"],
        "description": "alias for `chflags hidden PATH` and <code>chflags nohidden PATH</code>."
    },
    {
        "name": "latest_download",
        "description": "prints the path to the newest file in my Downloads folder"
    },
    {
        "usage": "reveal PATH",
        "description": "reveal the file/folder in the macOS Finder; alias for <code>open -R</code>"
    },
    {
        "name": "sizes",
        "description": """
        gets the total size of all the files/folders under the working directory, and prints them in a table
        <p><pre><code>$ sizes
        512.00K aws/
        520.00K wellcome/
          1.54M images/
          4.76M .git/
        -------
          7.58M ~/repos/scripts</code></pre></p>
        """
    },
]

cog_helpers.create_description_table(folder_name=folder_name, scripts=scripts)

]]]-->
<dl>
  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fs/cdir">
      <code>cdir</code>
    </a>
  </dt>
  <dd>
    counts all the entries in subfolders under the working directory, and prints them in a table
    <p><pre><code>$ cdir
     37 fishconfig
     48 repros
     51 colossus-wheels
     70 services
    292 .git
    -------
    699</code></pre></p>
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fs/deepestdir">
      <code>deepestdir [ROOT]</code>
    </a>
  </dt>
  <dd>
    prints the directory which is the deepest child of the given directory
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fs/emptydir.py">
      <code>emptydir.py</code>
    </a>
  </dt>
  <dd>
    removes any empty directories under the current one (including directories that are empty aside from files that can be safely deleted, e.g. <code>.DS_Store</code>)
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fs/flatten">
      <code>flatten</code>
    </a>
  </dt>
  <dd>
    flattens a directory structure.
    When you run it in a folder, it moves any files in subfolders into the top-level folders, then deletes the now-empty folder.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fs/hide">
      <code>hide [PATH]</code>
    </a>
/
    <a href="https://github.com/alexwlchan/scripts/blob/main/fs/unhide">
      <code>unhide [PATH]</code>
    </a>
  </dt>
  <dd>
    alias for `chflags hidden PATH` and <code>chflags nohidden PATH</code>.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fs/latest_download">
      <code>latest_download</code>
    </a>
  </dt>
  <dd>
    prints the path to the newest file in my Downloads folder
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fs/reveal">
      <code>reveal PATH</code>
    </a>
  </dt>
  <dd>
    reveal the file/folder in the macOS Finder; alias for <code>open -R</code>
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/fs/sizes">
      <code>sizes</code>
    </a>
  </dt>
  <dd>
    gets the total size of all the files/folders under the working directory, and prints them in a table
    <p><pre><code>$ sizes
    512.00K aws/
    520.00K wellcome/
      1.54M images/
      4.76M .git/
    -------
      7.58M ~/repos/scripts</code></pre></p>
  </dd>
</dl>
<!-- [[[end]]] (checksum: 632a7aa9e05edd9243371bf85c14b266) -->
