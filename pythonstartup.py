"""
Improve the Python REPL.

Inspired by this tweet by @nedbat:
https://twitter.com/nedbat/status/817827164443840512

Features:

*   Use pprint() by default.
    https://gist.github.com/chekunkov/848c3472d4b0bee69bccd2e77907a590
*   Blue chevrons
    http://www.jasonamyers.com/2017/default-to-pprint-python-repl/
*   Tab completion
    https://github.com/patrik-johansson/dotfiles/blob/master/.pythonstartup

"""

import pprint
import readline
import rlcompleter
import sys


def displayhook_pprint(o):
    """Display hook powered by pprint.
    https://www.python.org/dev/peps/pep-0217/
    """
    if o is None:
        return
    if sys.version_info[0] == 2:
        import __builtin__ as builtins
    else:
        import builtins
    # Set '_' to None to avoid recursion
    # https://docs.python.org/3/library/sys.html#sys.displayhook
    builtins._ = None
    pprint.pprint(o)
    builtins._ = o


sys.ps1 = "\033[0;34m>>> \033[0m"
sys.ps2 = "\033[1;34m... \033[0m"

sys.displayhook = displayhook_pprint

readline.parse_and_bind("tab: complete")
