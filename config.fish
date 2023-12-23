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


# Prepend any extra directories to my PATH variable.
#
# Note: I use this instead of `fish_add_path` because it updates a global
# `fish_user_paths` array in ~/.config/fish/fish_variables, but that makes
# it harder to see how/where my PATH is defined.
#
# Doing it this way means I get a fresh PATH in every shell, and it's
# only updated by the directives below.

function prepend_to_path
    if test (count $argv) -eq 0
        echo "Usage: prepend_to_path /path/to/directory"
        return 1
    end

    set -l new_path $argv[1]

    if test -d $new_path
        set -x PATH $new_path $PATH
    end
end


prepend_to_path ~/.cargo/bin

prepend_to_path /Library/Frameworks/Python.framework/Versions/3.12/bin

prepend_to_path ~/repos/scripts
prepend_to_path ~/repos/scripts/aws
prepend_to_path ~/repos/scripts/docker
prepend_to_path ~/repos/scripts/fs
prepend_to_path ~/repos/scripts/git
prepend_to_path ~/repos/scripts/images
prepend_to_path ~/repos/scripts/installers
prepend_to_path ~/repos/scripts/macos
prepend_to_path ~/repos/scripts/terraform
prepend_to_path ~/repos/scripts/text

prepend_to_path ~/repos/ttml2srt


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
function __auto_auto_activate_venv --on-variable PWD --description "Auto activate/deactivate virtualenv when I change directories"
    auto_activate_venv
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
__create_python_script_alias images/images_only_pdf.py
__create_python_script_alias images/srgbify.py
__create_python_script_alias images/reborder.py
__create_python_script_alias text/fix_twitter_thread.py
__create_python_script_alias text/noplaylist.py

__create_python_module_alias keyring
__create_python_module_alias yt-dlp
