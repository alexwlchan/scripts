# This tells fish to auto-activate my virtualenvs when I change directories.
#
# I have a fairly simple naming convention for my virtualenvs: I put
# them in the root of the Git repo for each project, and I always
# name them `~/.venv`.  This means it's pretty easy to work out if
# a virtualenv exists for the current directory.
#
# See https://alexwlchan.net/2023/fish-venv/
#
function auto_activate_venv --description "Auto activate/deactivate virtualenv when I change directories"

		# Get the top-level directory of the current Git repo (if any)
    set REPO_ROOT (git rev-parse --show-toplevel 2>/dev/null)

    # Case #1: cd'd from a Git repo to a non-Git folder
    #
    # There's no virtualenv to activate, and we want to deactivate any
    # virtualenv which is already active.
    if test -z "$REPO_ROOT"; and test -n "$VIRTUAL_ENV"
        deactivate
    end

    # Case #2: cd'd folders within the same Git repo
    #
    # The virtualenv for this Git repo is already activated, so there's
    # nothing more to do.
    if [ "$VIRTUAL_ENV" = "$REPO_ROOT/.venv" ]
        return
    end

    # Case #3: cd'd from a non-Git folder into a Git repo
    #
    # If there's a virtualenv in the root of this repo, we should
    # activate it now.
    if [ -d "$REPO_ROOT/.venv" ]
        source "$REPO_ROOT/.venv/bin/activate.fish" &>/dev/null
    end
end
