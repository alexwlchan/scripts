# pathscripts

This is a collection of useful scripts and tools I keep in my [PATH].
I use this Git repository to sync them across multiple computers.

I use scripts over shell config for a couple of reasons:

-   Individual scripts are more portable.
    I can send you a script and you can start using it immediately, even if you use a different shell.

-   I can use different languages.
    I'm not restricted to whatever my shell uses.

-   It makes my shell start faster.
    I use [fish], and I've noticed that if I write large fish config files, there's a noticeable delay between starting a shell and getting my first prompt.
    Using scripts means I have smaller config files, and I get a first prompt faster.

[PATH]: https://en.wikipedia.org/wiki/PATH_(variable)
[fish]: https://fishshell.com/

## Usage

Individual scripts have header comments explaining what they do.
Download them and add them to your PATH.

You can also clone this entire repo, then add it to your PATH, if you want to use all the scripts.

For example, I have the following code in [my fishconfig](https://github.com/alexwlchan/fishconfig/blob/main/config.fish#L5-L22):

```shell
set --global --export PATH $PATH \
  ~/repos/scripts \
  ~/repos/scripts/aws \
  ~/repos/scripts/git \
  ~/repos/scripts/installers \
  ~/repos/scripts/macos \
  ~/repos/scripts/terraform
```

## Organisation

A lot of these names are short, to minimise the typing I need to do, but then that makes their meaning utterly inscrutable to an outsider (e.g. what do `gp` or `tfi` do?).
To make it a bit easier to find, I've grouped them into a couple of top-level folders.

I add all the subfolders to my PATH so I don't need to remember how they're organised, but it might make it easier to find stuff!

## Contributors

My scripts include code written by other people, and in those cases I've [attributed the commit that added the code/script to multiple authors][trailer].
This is why several people who aren't me appear in then list of contributors, even though none of them have ever directly committed code.

You can see all the (documented) instances of other people's code by searching for the [Co-authored-by line][search] in my commits.

[trailer]: https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors#:~:text=In%20the%20text%20box%20below,Commit%20changes%20or%20Propose%20changes.
[search]: https://github.com/search?q=repo%3Aalexwlchan%2Fscripts%20co-authored-by&type=commits
