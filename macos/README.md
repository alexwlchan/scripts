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
        "name": "get_live_text [image]",
        "description": "get OCR'd text for a single image using Live Text"
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
<a href="https://github.com/alexwlchan/scripts/blob/main/macos/get_live_text [image]">
<code>get_live_text [image]</code>
</a>
</dt>
<dd>
get OCR'd text for a single image using Live Text
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
<!-- [[[end]]] (checksum: 7185b51098c3e95c9d1fc51f860b1dd2) -->
