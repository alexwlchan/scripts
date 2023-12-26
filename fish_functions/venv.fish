# Create and activate a new virtualenv.
#
# This is to prevent me from making a very common mistake, which is
# creating the venv and then immediately running "pip install" without
# activating it first.
#
# See https://alexwlchan.net/2023/fish-venv/
#
function venv --description "Create and activate a new virtual environment"
    echo "Creating virtual environment in "(pwd)"/.venv"
    python3 -m venv .venv --upgrade-deps
    source .venv/bin/activate.fish

    # Append .venv to the Git exclude file, but only if it's not
    # already there.
    if test -e .git
        append_to_file_if_not_exists ".git/info/exclude" ".venv"
    end
end
