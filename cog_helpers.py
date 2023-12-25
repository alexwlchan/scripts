"""
Some helper functions for generating the README files in this repo.
In particular, it can take a list of scripts as a Python object, and
create an HTML definition list that describes them in a human-readable way.

Here Cog is Ned Batchelder's file generation tool, described here:
https://nedbatchelder.com/code/cog
"""

import textwrap
from typing import TypedDict

import cog


class ScriptWithName(TypedDict):
    name: str
    description: str


class ScriptWithUsage(TypedDict):
    usage: str
    description: str


Script = ScriptWithName | ScriptWithUsage


def create_description_table(
    folder_name: str,
    scripts: list[Script],
    repo_name: str = "alexwlchan/scripts",
    primary_branch: str = "main",
) -> None:
    cog.outl("<dl>")

    for s in scripts:
        try:
            name = s["name"]
        except KeyError:
            name = s["usage"].split()[0]

        try:
            usage = s["usage"]
        except KeyError:
            usage = name

        cog.outl("<dt>")
        cog.outl(
            f'<a href="https://github.com/{repo_name}/blob/{primary_branch}/{folder_name}/{name}">'
        )
        cog.outl(f"<code>{usage}</code>")
        cog.outl("</a>")
        cog.outl("</dt>")

        cog.outl("<dd>")
        cog.outl(textwrap.dedent(s["description"]).strip())
        cog.outl("</dd>")

    cog.outl("</dl>")
