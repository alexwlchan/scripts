# Create and activate a new virtualenv.
#
# This is to prevent me from making a very common mistake, which is
# creating the venv and then immediately running "pip install" without
# activating it first.
function venv
    echo "Creating virtual environment in "(pwd)"/.venv"
    python3 -m venv .venv --upgrade-deps

    if [ -f .git ]
        echo .venv >>.git/info/exclude
    end

    source .venv/bin/activate.fish
end
