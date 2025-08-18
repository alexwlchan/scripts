# scripts

This is a collection of various scripts and tools I find useful.

I manage them in a Git repository to ensure I have a consistent setup across different computers.

## Installation

To set up this repo on a new computer, I run the following commands in a Fish shell:

1.  Clone the repository:

    ```console
    $ git clone git@github.com:alexwlchan/scripts.git ~/repos/scripts
    $ cd ~/repos/scripts
    ```

2.  Create a Python virtualenv and install dependencies:

    ```console
    $ python3 -m venv .venv
    $ source .venv/bin/activate.fish
    $ uv pip install -r requirements.txt
    ```
    
3.  Install my Fish config, so Fish knows where to find all these scripts:

    ```console
    $ ln -s ~/repos/scripts/config.fish ~/.config/fish/config.fish
    ```

## Organisation

A lot of these names are short, to minimise the typing I need to do, but then that makes their meaning utterly inscrutable to an outsider (e.g. what do `gp` or `tfi` do?).
To make it a bit easier to find, I've grouped them into a couple of top-level folders.

I add all the subfolders to my PATH so I don't need to remember how they're organised, but it might make it easier to find stuff!

## What goes in this repo

The script in this repo are pretty short – typically 50 lines or less (including documentation).
They're mostly stuff that I can write all in one go.

If a script gets sufficiently large and complicated that it might benefit from its own documentation or change history, it "graduates" into a separate repo.
