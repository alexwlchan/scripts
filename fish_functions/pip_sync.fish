function pip_sync --description "Make a virtualenv dependencies look like requirements.txt"

    # If there isn't a virtualenv already, create one
    if test -z "$VIRTUAL_ENV"
        venv
    end

    # If there are no `requirements.txt` files, run my `pip compile`
    # script to create a set of version pins.
    if not test -e requirements.txt; and not test -e dev_requirements.txt; or contains -- --compile $argv;
        or contains -- --upgrade $argv
        pip_compile $argv

        echo ""
    end

    # If we're on an external disk, disable the warning about being
    # unable to clone files.  In particular:
    #
    #     warning: Failed to clone files; falling back to full copy.
    #     This may lead to degraded performance.  If the cache and target 
    #     directories are on different filesystems, reflinking may not
    #     be supported.
    #
    #     If this is intentional, set `export UV_LINK_MODE=copy` or use 
    #     `--link-mode=copy` to suppress this warning.
    #
    # On macOS, this means "are you in a path that starts with /Volumes".
    if string match -q "/Volumes/*" "$PWD"
        set -x UV_LINK_MODE copy
    end

    # Actually run the `uv pip sync` command.
    run_pip_sync $argv
end
