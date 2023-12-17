# This tells fish to auto-enable my virtualenvs when I change directories.
#
# I have a fairly simple naming convention for my virtualenvs: I put
# them in the root of the Git repo for each project, and I always
# name them `~/.venv`.  This means it's pretty easy to work out if
# a virtualenv exists for the current directory.
function auto_enable_venv
    set REPO_ROOT (git rev-parse --show-toplevel 2>/dev/null)

    # If we're not inside a Git repo, there's no virtualenv to activate.
    #
    # If we're already in a virtualenv, then we want to deactivate it
    # (e.g. we've switched from a Git repo to another directory).
    # Otherwise there's nothing to do.
    if test -z "$REPO_ROOT"; and test -n "$VIRTUAL_ENV"
        deactivate
    end

    # If we're inside a Git repo, we look for the presence of .venv
    # in the root.  We may already have the venv activated, in which
    # case there's nothing to do.
    if [ "$VIRTUAL_ENV" = "$REPO_ROOT/.venv" ]
        return
    end

    if [ -d "$REPO_ROOT/.venv" ]
        source "$REPO_ROOT/.venv/bin/activate.fish" &>/dev/null
    end
end
