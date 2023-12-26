"""
Some helper functions for generating the README files in this repo.
In particular, it can take a list of scripts as a Python object, and
create an HTML definition list that describes them in a human-readable way.

Here Cog is Ned Batchelder's file generation tool, described here:
https://nedbatchelder.com/code/cog
"""

import textwrap
from typing import Literal, TypedDict

import cog


class ScriptWithName(TypedDict):
    name: str
    description: str


class ScriptWithUsage(TypedDict):
    usage: str
    description: str


Script = ScriptWithName | ScriptWithUsage


def outl(s: str, indent: int = 0):
    cog.outl(textwrap.indent(s, prefix=' ' * indent))


def create_description_table(
    folder_name: str,
    scripts: list[Script],
    repo_name: str = "alexwlchan/scripts",
    primary_branch: str = "main",
) -> None:
    indent = 0

    outl("<dl>")

    for i, s in enumerate(scripts, start=1):
        try:
            name = s["name"]
        except KeyError:
            name = s["usage"].split()[0]

        try:
            usage = s["usage"]
        except KeyError:
            usage = name

        outl("<dt>", indent=2)
        outl(
            f'<a href="https://github.com/{repo_name}/blob/{primary_branch}/{folder_name}/{name}">',
            indent=4
        )
        outl(f"<code>{usage}</code>", indent=6)
        outl("</a>", indent=4)
        outl("</dt>", indent=2)

        outl("<dd>", indent=2)
        outl(textwrap.dedent(s["description"]).strip(), indent=4)
        outl("</dd>", indent=2)

        if i != len(scripts):
            outl("")

    outl("</dl>")
