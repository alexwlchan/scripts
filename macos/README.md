# macos

These scripts are all for doing stuff on macOS.
They rely on Mac-specific stuff and are unlikely to be useful on non-Mac systems.

## The individual scripts

<!-- [[[cog

# This adds the root of the repo to the PATH, which has cog_helpers.py
from os.path import abspath, dirname
import sys; sys.path.append(abspath(dirname(dirname("."))))

import cog_helpers

folder_name = "macos"

scripts = [
    {
        "name": "battery",
        "description": "alias for <code>pmset -g batt</code>; reports the current battery level",
    },
    {
        "name": "close_tabs",
        "description": "close ephemeral tabs in Safari – basically, anything that can be easily recreated/reopened later."
    },
    {
        "usage": "close_specific_tabs [example.org fragment.net]",
        "description": "close tabs in Safari based on their URL – useful for closing tabs which I can see have high activity/CPU in Activity Monitor."
    },
    {
        "name": "count_tabs",
        "description": "count the number of tabs I have open in Safari."
    },
    {
        "name": "ffile",
        "description": "print the path to the frontmost selected item in Finder"
    },
    {
        "name": "furl",
        "description": "get the URL of the frontmost Safari window"
    },
    {
        "name": "find_processes_using_secure_input",
        "description": "lists any processes using Secure Input, which can block apps like TextExpander"
    },
    {
        "usage": "get_all_live_text [directory]",
        "description": "get OCR'd text for all the images in a directory using Live Text"
    },
    {
        "name": "get_focus_mode",
        "description": "prints the current Focus mode"
    },
    {
        "name": "get_photo_sizes",
        "description": "print the size of every item in my Photos Library."
    },
    {
        "name": "list_safari_tabs",
        "description": "print the URL of every tab I have open in Safari"
    },
    {
        "name": "obnote",
        "description": "print the path to the note I currently have open in [Obsidian](https://obsidian.md/), if any."
    },
    {
        "usage": "set_accent_colour (red|orange|yellow|green|blue|purple|pink|graphite)",
        "description": "set the accent colour, as configured in the Appearance settings",
    },
    {
        "usage": "sterilise [PATH]",
        "description": "alias for <code>xattr -d com.apple.quarantine</code>"
    },
    {
        "usage": "trash [PATH]",
        "description": "move a file to the Trash"
    },
    {
        "name": "unlock_keychain",
        "description": """
        alias for <code>security unlock-keychain ~/Library/Keychains/login.keychain</code>; unlocks the login keychain
        <p>
          The login keychain normally gets unlocked by the OS when you log into your account; this is for when I'm accessing a Mac over SSH.
        </p>
        """
    }
]

cog_helpers.create_description_table(folder_name=folder_name, scripts=scripts)

]]]-->
<dl>
  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/battery">
      <code>battery</code>
    </a>
  </dt>
  <dd>
    alias for <code>pmset -g batt</code>; reports the current battery level
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/close_tabs">
      <code>close_tabs</code>
    </a>
  </dt>
  <dd>
    close ephemeral tabs in Safari – basically, anything that can be easily recreated/reopened later.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/close_specific_tabs">
      <code>close_specific_tabs [example.org fragment.net]</code>
    </a>
  </dt>
  <dd>
    close tabs in Safari based on their URL – useful for closing tabs which I can see have high activity/CPU in Activity Monitor.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/count_tabs">
      <code>count_tabs</code>
    </a>
  </dt>
  <dd>
    count the number of tabs I have open in Safari.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/ffile">
      <code>ffile</code>
    </a>
  </dt>
  <dd>
    print the path to the frontmost selected item in Finder
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/furl">
      <code>furl</code>
    </a>
  </dt>
  <dd>
    get the URL of the frontmost Safari window
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/find_processes_using_secure_input">
      <code>find_processes_using_secure_input</code>
    </a>
  </dt>
  <dd>
    lists any processes using Secure Input, which can block apps like TextExpander
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/get_all_live_text">
      <code>get_all_live_text [directory]</code>
    </a>
  </dt>
  <dd>
    get OCR'd text for all the images in a directory using Live Text
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/get_focus_mode">
      <code>get_focus_mode</code>
    </a>
  </dt>
  <dd>
    prints the current Focus mode
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/get_photo_sizes">
      <code>get_photo_sizes</code>
    </a>
  </dt>
  <dd>
    print the size of every item in my Photos Library.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/list_safari_tabs">
      <code>list_safari_tabs</code>
    </a>
  </dt>
  <dd>
    print the URL of every tab I have open in Safari
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/obnote">
      <code>obnote</code>
    </a>
  </dt>
  <dd>
    print the path to the note I currently have open in [Obsidian](https://obsidian.md/), if any.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/set_accent_colour">
      <code>set_accent_colour (red|orange|yellow|green|blue|purple|pink|graphite)</code>
    </a>
  </dt>
  <dd>
    set the accent colour, as configured in the Appearance settings
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/sterilise">
      <code>sterilise [PATH]</code>
    </a>
  </dt>
  <dd>
    alias for <code>xattr -d com.apple.quarantine</code>
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/trash">
      <code>trash [PATH]</code>
    </a>
  </dt>
  <dd>
    move a file to the Trash
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/macos/unlock_keychain">
      <code>unlock_keychain</code>
    </a>
  </dt>
  <dd>
    alias for <code>security unlock-keychain ~/Library/Keychains/login.keychain</code>; unlocks the login keychain
    <p>
      The login keychain normally gets unlocked by the OS when you log into your account; this is for when I'm accessing a Mac over SSH.
    </p>
  </dd>
</dl>
<!-- [[[end]]] (checksum: dd3558b095357994d6bd03ab9bdc8481) -->
