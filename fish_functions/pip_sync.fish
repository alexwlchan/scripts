function pip_sync --description "Make a virtualenv dependencies look like requirements.txt"

    # Run the `pip compile` script to get a set of version pins.
    if contains -- --upgrade $argv
        pip_compile --upgrade
    else
        pip_compile
    end

    # If there isn't a virtualenv already, create one
    if test -z "$VIRTUAL_ENV"
        venv
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
        set UV_LINK_MODE copy
    end

    # Actually run the `uv pip sync` command.
    #
    # If a dev_requirements.txt file is available, use that, otherwise use 
    # the standard `requirements.txt`.
    if test \( -e dev_requirements.txt \)
        ~/repos/scripts/debug/print_info "-> uv pip sync dev_requirements.txt"
        uv pip sync dev_requirements.txt
    else if test \( -e requirements.txt \)
        ~/repos/scripts/debug/print_info "-> uv pip sync requirements.txt"
        uv pip sync requirements.txt
    end
end
