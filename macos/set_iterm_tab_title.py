#!/usr/bin/env python3
"""
Set the title of an iTerm 2 tab.
"""

import sys

import iterm2


def set_title(title: str):
    async def main(connection: iterm2.connection.Connection) -> None:
        app = await iterm2.async_get_app(connection)

        window = app.current_window
        if window is None:
            return

        tab = window.current_tab
        if tab is None:
            return

        await tab.async_set_title(title)

    iterm2.run_until_complete(main)


if __name__ == "__main__":
    try:
        title = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} TITLE")

    set_title(title)
