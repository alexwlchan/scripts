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


# Taken from https://gist.github.com/tommyip/cf9099fa6053e30247e5d0318de2fb9e
#
# This will automatically enable/disable my virtualenvs when I enter/leave directories.
#
# Based on https://gist.github.com/bastibe/c0950e463ffdfdfada7adf149ae77c6f
# Changes:
# * Instead of overriding cd, we detect directory change. This allows the script to work
#   for other means of cd, such as z.
# * Update syntax to work with new versions of fish.
# * Handle virtualenvs that are not located in the root of a git directory.

function __auto_source_venv --on-variable PWD --description "Activate/Deactivate virtualenv on directory change"
    status --is-command-substitution; and return

    # Check if we are inside a git directory
    if git rev-parse --show-toplevel &>/dev/null
        set gitdir (realpath (git rev-parse --show-toplevel))
        set cwd (pwd)
        # While we are still inside the git directory, find the closest
        # virtualenv starting from the current directory.
        while string match "$gitdir*" "$cwd" &>/dev/null
            if test -e "$cwd/.venv/bin/activate.fish"
                source "$cwd/.venv/bin/activate.fish" &>/dev/null
                return
            else
                set cwd (path dirname "$cwd")
            end
        end
    end

    # If virtualenv activated but we are not in a git directory, deactivate.
    if test -n "$VIRTUAL_ENV"
        deactivate
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
