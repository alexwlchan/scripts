# Create and activate a new virtualenv.
#
# This is to prevent me from making a very common mistake, which is
# creating the venv and then immediately running "pip install" without
# activating it first.
#
# This has to be a fish function, because I'm activating the venv.
#
# See https://alexwlchan.net/2023/fish-venv/
#
function venv --description "Create and activate a new virtual environment"

    # I don't want venvs in my home directory; block it if I try
    if test "$PWD" = "$HOME"
        cd $(mktemp -d)
    end

    # I never want to create a virtual environment in the top level of
    # one of my external volumes; block it if I try -- it means I've
    # run a command in the wrong directory.
    if test (dirname "$PWD") = /Volumes
        print_error "Can’t create a virtualenv in $PWD!"
        return 1
    end

    print_info "Creating virtual environment in "(pwd)"/.venv"
    uv venv --quiet .venv
    source .venv/bin/activate.fish
    print_info "Using: "(python3 --version)

    # Append .venv to the Git exclude file, but only if it's not
    # already there.
    if test -e .git
        append_to_file_if_not_exists ".git/info/exclude" ".venv"
    end

    # Tell Time Machine that it doesn't need to both backing up the
    # virtualenv directory.
    #
    # Note: this is quite slow, so we only run it if we're in my home
    # directory -- it won't get backed up otherwise.
    if string match -q "$HOME/*" "$PWD"
        tmutil addexclusion .venv
    end
end
