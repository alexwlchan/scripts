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


# Add any extra directories to my PATH variable.
fish_add_path /Library/Frameworks/Python.framework/Versions/3.12/bin

fish_add_path ~/repos/scripts
fish_add_path ~/repos/scripts/aws
fish_add_path ~/repos/scripts/docker
fish_add_path ~/repos/scripts/fs
fish_add_path ~/repos/scripts/git
fish_add_path ~/repos/scripts/installers
fish_add_path ~/repos/scripts/macos
fish_add_path ~/repos/scripts/terraform
fish_add_path ~/repos/scripts/text

fish_add_path ~/repos/private-scripts/.with-venv-python

fish_add_path ~/repos/ttml2srt


# This prevents me from installing packages with pip without being
# in a virtualenv first.
#
# This allows me to keep my system Python clean, and install all my
# packages inside virtualenvs.
#
# See https://docs.python-guide.org/dev/pip-virtualenv/#requiring-an-active-virtual-environment-for-pip
#
set -g -x PIP_REQUIRE_VIRTUALENV true


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


# These functions run scripts in this repo using the virtualenv, rather
# than running them with system Python.
#
# e.g. emptydir.py relies on the `humanize` library.  That isn't installed
# in my system Python, but it is installed in my `scripts` virtualenv.
#
# Useful reading: https://github.com/fish-shell/fish-shell/issues/1776

function __create_bash_script_alias
    set script_path $argv[1]
    set shortcut (path basename (path change-extension '' $script_path))

    function $shortcut --inherit-variable script_path
        set existing_venv "$VIRTUAL_ENV"

        source ~/repos/scripts/.venv/bin/activate.fish
        bash ~/repos/scripts/$script_path $argv

        # If we were in a virtualenv before we started running this
        # script, make sure we re-enable it afterwards.
        #
        # If not, we just need to deactivate the scripts venv.
        if [ existing_venv = "" ]
            source "$existing_venv/bin/activate.fish"
        else
            deactivate
        end
    end
end

function __create_python_script_alias
    set script_path $argv[1]
    set shortcut (path basename (path change-extension '' $script_path))

    function $shortcut --inherit-variable script_path
        ~/repos/scripts/.venv/bin/python3 ~/repos/scripts/$script_path $argv
    end
end

function __create_python_module_alias
    set module_name $argv[1]

    eval "alias $module_name=\"~/repos/scripts/.venv/bin/$module_name\""
end

__create_bash_script_alias flickr/flapi.sh
__create_bash_script_alias flickr/flphoto.sh

__create_python_script_alias flickr/fluser_lookup.py
__create_python_script_alias fs/emptydir.py
__create_python_script_alias git/git-cloc.py
__create_python_script_alias images/kn_cover_image.py
__create_python_script_alias images/srgbify.py
__create_python_script_alias text/noplaylist.py
__create_python_script_alias text/reborder.py

__create_python_module_alias keyring
__create_python_module_alias yt-dlp
