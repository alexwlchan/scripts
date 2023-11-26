# Don't show a greeting on startup.  In particular, don't show
# this message:
#
#     Welcome to fish, the friendly interactive shell
#     Type help for instructions on how to use fish
#
set -g -x fish_greeting ''


# This tells fish to find functions in my "fish_functions" directory.
#
# Note that we have to *prepend* the directory in this repo, so we
# can override the built-in functions.  e.g. I want to use the definition
# of `fish_prompt` from this repo, rather than the default versions
#
# See https://fishshell.com/docs/current/language.html#autoloading-functions
#
set -x fish_function_path ~/repos/scripts/fish_functions $fish_function_path


# This tells fish to run a couple of functions as event handlers --
# that is, to run a function when a variable changes or something similar.
# These functions can't be autoloaded.
#
# See https://fishshell.com/docs/current/language.html#event
#
function __auto_enable_venv --on-variable PWD
    auto_enable_venv
end


# Load macOS-specific utilities
if [ (uname -s) = Darwin ]
    # Provide a convenient alias for the front URL in both browsers
    alias furl="safari url"
    alias gurl="osascript -e 'tell application \"Google Chrome\" to tell front window to get URL of tab (active tab index)'"

    # Get the URL of the frontmost GitHub page and clone it
    function gh-clone
        _ensure_ssh_key_loaded
        github-clone (furl)
    end
end


# These aliases run scripts in this repo using the virtualenv, rather
# than running them with system Python.
#
# e.g. emptydir.py relies on the `humanize` library.  That isn't installed
# in my system Python, but it is installed in my `scripts` virtualenv.
#
function __run_in_scripts_venv
    ~/repos/scripts/.venv/bin/python3 ~/repos/scripts/$argv[1] $argv[2..]
end

alias emptydir="__run_in_scripts_venv fs/emptydir.py"
alias flapi="__run_in_scripts_venv flickr/flapi.sh"
alias flphoto="__run_in_scripts_venv flickr/flphoto.sh"
alias kn_cover_image="__run_in_scripts_venv images/kn_cover_image.py"
alias noplaylist="__run_in_scripts_venv text/noplaylist.py"
alias reborder="__run_in_scripts_venv images/reborder.py"
alias srgbify="__run_in_scripts_venv images/srgbify.py"
