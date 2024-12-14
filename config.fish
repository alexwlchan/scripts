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
# == Why not use `fish_add_path`? ==
#
# That function updates a global `fish_user_paths` array in a file which
# isn't tracked by Git: `~/.config/fish/fish_variables`.  That makes it
# harder to see how/where my PATH is defined.
#
# For example, I could have removed the code that adds a directory to
# my PATH from this repo, but it would persist in the `fish_variables` file.
#
# Using my own function means I get a fresh PATH in every shell, and it's
# only updated by the directives below.  All my PATH additions can be
# tracked in Git.

function prepend_to_path
    if test (count $argv) -eq 0
        echo "Usage: prepend_to_path /path/to/directory"
        return 1
    end

    set --local new_path $argv[1]

    if test -d $new_path
        set --export PATH $new_path $PATH
    end
end

prepend_to_path ~/repos/scripts
prepend_to_path ~/repos/scripts/aws
prepend_to_path ~/repos/scripts/flickr
prepend_to_path ~/repos/scripts/fs
prepend_to_path ~/repos/scripts/git
prepend_to_path ~/repos/scripts/images
prepend_to_path ~/repos/scripts/installers
prepend_to_path ~/repos/scripts/macos
prepend_to_path ~/repos/scripts/terraform
prepend_to_path ~/repos/scripts/text
prepend_to_path ~/repos/scripts/web

prepend_to_path ~/repos/flapi.sh

prepend_to_path ~/.local/bin

# Path for Rust
prepend_to_path ~/.cargo/bin

# Paths for Ruby and bundler
#
# These paths are different for Intel/Apple Silicon Macs.
prepend_to_path /opt/homebrew/bin
prepend_to_path /opt/homebrew/opt/ruby/bin
prepend_to_path /opt/homebrew/lib/ruby/gems/3.3.0/bin



# Prepend any Homebrew-related directories to my PATH variable.
#
# Note that Homebrew installs into different directories depending on
# whether you're on an Intel or Apple Silicon Mac.  Eventually I can
# delete this when I get rid of my last Intel Mac, but until then
# I want to make sure I have the same paths on both machines.
#
# See https://docs.brew.sh/Installation

if test (uname -m) = "arm64"
  set HOMEBREW_PREFIX /opt/homebrew
else
  set HOMEBREW_PREFIX /usr/local
end

prepend_to_path $HOMEBREW_PREFIX/bin
prepend_to_path $HOMEBREW_PREFIX/opt/ruby/bin


# This prevents me from installing packages with pip without being
# in a virtualenv first.
#
# This allows me to keep my system Python clean, and install all my
# packages inside virtualenvs.
#
# See https://docs.python-guide.org/dev/pip-virtualenv/#requiring-an-active-virtual-environment-for-pip
# See https://alexwlchan.net/# See https://alexwlchan.net/2023/fish-venv/
#
set -g -x PIP_REQUIRE_VIRTUALENV true


# This points to a file which will be run as a setup script any time
# I start an interactive Python session.  It customises the prompt slightly
# and adds tab completion.
#
# See https://docs.python.org/3/using/cmdline.html#envvar-PYTHONSTARTUP
#
set -g -x PYTHONSTARTUP ~/repos/scripts/pythonstartup.py


# This tells fish to run a couple of functions as event handlers --
# that is, to run a function when a variable changes or something similar.
# These functions can't be autoloaded.
#
# See https://fishshell.com/docs/current/language.html#event
# See https://alexwlchan.net/2023/fish-venv/
#
function __auto_activate_venv --on-variable PWD --description "Auto activate/deactivate virtualenv when I change directories"
    auto_activate_venv
end


# This updates the Git index whenever I 'cd' into a new directory.
#
# Not all directories are Git repos, so if it returns an error, hide it.
#
# This is needed for showing my Git branch in my prompt: otherwise I see
# an asterisk for uncommitted changes until I interact with Git somehow,
# even though there aren't any.
function __refresh_git_indexes --on-variable PWD
    git update-index --refresh >/dev/null 2>&1
end


# Load macOS-specific utilities
if [ (uname -s) = Darwin ]
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
        if test -z "$existing_venv"
            deactivate
        else
            source "$existing_venv/bin/activate.fish"
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

__create_bash_script_alias text/pp_xml.sh

__create_python_script_alias fs/cdir.py
__create_python_script_alias git/find_big_commits.py
__create_python_script_alias git/git-cloc.py
__create_python_script_alias images/chunky_pixels.py
__create_python_script_alias images/copycrop.py
__create_python_script_alias images/kn_cover_image.py
__create_python_script_alias images/images_only_pdf.py
__create_python_script_alias images/pdfthumb.py
__create_python_script_alias images/reborder.py
__create_python_script_alias images/save_xkcd.py
__create_python_script_alias images/srgbify.py
__create_python_script_alias images/tint_image.py
__create_python_script_alias text/fix_twemoji.py
__create_python_script_alias text/fix_twitter_thread.py
__create_python_script_alias text/natsize.py
__create_python_script_alias text/noplaylist.py
__create_python_script_alias text/sumsizes.py
__create_python_script_alias web/download_instagram.py
__create_python_script_alias web/yt-dlp.py
