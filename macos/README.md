# macos

These scripts are all for doing stuff on macOS.
They rely on Mac-specific stuff and are unlikely to be useful on non-Mac systems.

## The individual scripts

<!-- [[[cog

import sys; sys.path.append("/Users/alexwlchan/repos/scripts")
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
</dl>
<!-- [[[end]]] (checksum: fa3a0dacc7ecb411506845102787c6ae) -->
