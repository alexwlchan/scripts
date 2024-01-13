"""
Some helper functions for generating the README files in this repo.
In particular, it can take a list of scripts as a Python object, and
create an HTML definition list that describes them in a human-readable way.

Here Cog is Ned Batchelder's file generation tool, described here:
https://nedbatchelder.com/code/cog
"""

import os
import textwrap
from typing import TypedDict

import cog


class ScriptWithName(TypedDict):
    name: str
    description: str


class ScriptWithVariants(TypedDict):
    variants: list[str]
    description: str


class ScriptWithUsage(TypedDict):
    usage: str
    description: str


Script = ScriptWithName | ScriptWithUsage | ScriptWithVariants


def outl(s: str, indent: int = 0):
    cog.outl(textwrap.indent(s, prefix=" " * indent))


def create_description_table(
    folder_name: str,
    scripts: list[Script],
    repo_name: str = "alexwlchan/scripts",
    primary_branch: str = "main",
    ignore_files: set[str] | None = None,
) -> None:
    documented_files = set()

    if ignore_files is None:
        ignore_files = set()

    outl("<dl>")

    for i, s in enumerate(scripts, start=1):
        if "name" in s:
            variants = [s["name"]]
        elif "variants" in s:
            variants = s["variants"]
        else:
            variants = [s["usage"].split()[0]]

        outl("<dt>", indent=2)

        for index, v in enumerate(variants, start=1):
            name = v.split()[0]

            path = os.path.join(folder_name, name)
            assert os.path.exists(path), os.path.join(path)

            documented_files.add(name)

            outl(
                f'<a href="https://github.com/{repo_name}/blob/{primary_branch}/{folder_name}/{name}">',
                indent=4,
            )

            try:
                usage = s["usage"]
            except KeyError:
                usage = v

            outl(f"<code>{usage}</code>", indent=6)
            outl("</a>", indent=4)

            if index != len(variants):
                outl("/")

        outl("</dt>", indent=2)

        outl("<dd>", indent=2)
        outl(textwrap.dedent(s["description"]).strip(), indent=4)
        outl("</dd>", indent=2)

        if i != len(scripts):
            outl("")

    outl("</dl>")

    # Now check there isn't anything in the folder which should have
    # been documented, but isn't.
    undocumented_files = set()

    for f in os.listdir(folder_name):
        if os.path.isdir(os.path.join(folder_name, f)):
            continue

        if f in {"README.md", "utf8info.Dockerfile"}:
            continue

        if f.startswith(("test_", "_", ".")):
            continue

        if f.endswith((".png", ".db")):
            continue

        if f in ignore_files:
            continue

        if f not in documented_files:
            undocumented_files.add(f)

    if undocumented_files:
        raise ValueError(
            f"Not all files in {folder_name} are documented: {undocumented_files}"
        )
