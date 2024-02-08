# textexpander

These scripts I invoke as text expansion macros in [TextExpander](https://textexpander.com/).

## The individual scripts

<!-- [[[cog

# This adds the root of the repo to the PATH, which has cog_helpers.py
from os.path import abspath, dirname
import sys

sys.path.append(abspath(dirname(dirname("."))))

import cog_helpers

folder_name = "textexpander"

scripts = [
    {
        "name": "copy_file_into_obsidian.py",
        "description": """
        get the latest download from my Desktop, copy it into Obsidian, and print a ![[…]] link to insert it into my current document.
        """
    },
    {
        "name": "create_books_commit_message",
        "description": """
        create a commit message for when I'm adding new books to my book tracker.
        """
    },
    {
        "name": "create_til_commit_message",
        "description": """
        create a commit message for when I'm updating my TIL (Today-I-Learned) repository.
        """
    },
    {
        "name": "get_markdown_link.py",
        "description": """
        print a reference-style Markdown link to my frontmost Safari URL
        """,
    },
    {
        "name": "get_mastodon_text.py",
        "description": """
        print a Markdown-formatted blockquote of a Mastodon I've got open in Safari, suitable for saving in Obsidian
        """,
    },
    {
        "name": "get_wikipedia_quote.py",
        "description": """
        get URL and first paragraph of a Wikipedia entry I have open in Safari, suitable for saving in Obsidian.
        """,
    },
]

cog_helpers.create_description_table(
    folder_name=folder_name,
    scripts=scripts,
    ignore_files={"urls.py"}
)

]]]-->
<dl>
  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/textexpander/copy_file_into_obsidian.py">
      <code>copy_file_into_obsidian.py</code>
    </a>
  </dt>
  <dd>
    get the latest download from my Desktop, copy it into Obsidian, and print a ![[…]] link to insert it into my current document.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/textexpander/create_books_commit_message">
      <code>create_books_commit_message</code>
    </a>
  </dt>
  <dd>
    create a commit message for when I'm adding new books to my book tracker.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/textexpander/create_til_commit_message">
      <code>create_til_commit_message</code>
    </a>
  </dt>
  <dd>
    create a commit message for when I'm updating my TIL (Today-I-Learned) repository.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/textexpander/get_markdown_link.py">
      <code>get_markdown_link.py</code>
    </a>
  </dt>
  <dd>
    print a reference-style Markdown link to my frontmost Safari URL
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/textexpander/get_mastodon_text.py">
      <code>get_mastodon_text.py</code>
    </a>
  </dt>
  <dd>
    print a Markdown-formatted blockquote of a Mastodon I've got open in Safari, suitable for saving in Obsidian
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/textexpander/get_wikipedia_quote.py">
      <code>get_wikipedia_quote.py</code>
    </a>
  </dt>
  <dd>
    get URL and first paragraph of a Wikipedia entry I have open in Safari, suitable for saving in Obsidian.
  </dd>
</dl>
<!-- [[[end]]] (checksum: 75dbd3e0c7b1be65eb5c169399792cc4) -->
