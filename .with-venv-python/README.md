This folder contains aliases for my Python scripts that causes them to run in a scripts-repo virtual environment, rather than my global Python.

There's unlikely to be anything here which is useful to anyone but me.

## Why?

I try to run everything inside virtual environments, and not install any dependencies globally.
I used to install my dependencies with the `--user` flag, but [Glyph's article](https://blog.glyph.im/2023/08/get-your-mac-python-from-python-dot-org.html) persuaded me to change my ways.
For several reasons:

*   Don't pollute my global Python installation
*   Make it easier to track which library versions I'm using (there are some scripts I go for years on end without using, and it's annoying if I don't have a record of what library version I originally wrote them with)
*   Better isolation of different projects

I have a single virtualenv on my Mac for my scripts (`~/repos/scripts/.venv`).

I could point to that Python in the shebang at the top of my scripts:

```console
$ cat myscript
#!/Users/alexwlchan/repos/scripts/.venv/bin/python3
"""
This script is for ...
```

but that's quite fragile and makes the scripts less portable.

So instead, I save the scripts as `[scriptname].py`, then create an alias `[scriptname]` in this folder which runs my script inside the virtual environment:

```console
$ cat myscript.py
#!/usr/bin/env python3
"""
This script is for ...

$ cat myscript
#!/usr/bin/env bash

set -o errexit
set -o nounset

~/repos/scripts/.venv/bin/python3 "~/repos/scripts/images/[myscript].py" "$@"
```
