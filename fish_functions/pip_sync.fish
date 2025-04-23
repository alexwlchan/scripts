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
    
    echo ""

    if test \( -e dev_requirements.txt \)
        ~/repos/scripts/debug/print_info "-> uv pip sync dev_requirements.txt"
        uv pip sync dev_requirements.txt
    else if test \( -e requirements.txt \)
        ~/repos/scripts/debug/print_info "-> uv pip sync requirements.txt"
        uv pip sync requirements.txt
    end
end
