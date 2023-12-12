# Create and activate a new virtualenv.
#
# This is to prevent me from making a very common mistake, which is
# creating the venv and then immediately running "pip install" without
# activating it first.
function venv
    echo "Creating virtual environment in "(pwd)"/.venv"
    python3 -m venv .venv --upgrade-deps

    if test -e .git
        echo .venv >>.git/info/exclude
    end

    source .venv/bin/activate.fish

    echo "Updating to the latest version of pip"
    pip install --upgrade pip

    # If we're in a trusted Git repository (one that I own) and we
    # can see  a requirements file, go ahead and install pip-tools
    # and install the dependencies.
    if test -e .git
        set remote_url (git remote get-url origin)

        set -a trusted_orgs "Flickr-Foundation" "alexwlchan"

        for org in $trusted_orgs
            if ! string match -q -- "git@github.com:$org/*" "$remote_url"
                continue
            end

            echo "This repo is in in a trusted org; looking for dependencies"

            if test -f dev_requirements.txt
                echo "Installing dependencies from dev_requirements.txt"
                pip install pip-tools
                pip-sync dev_requirements.txt
            else if test -f requirements.txt
                echo "Installing dependencies from requirements.txt"
                pip install pip-tools
                pip-sync requirements.txt
            else
                echo "No requirements.txt file found; no dependencies installed"
            end
        end
    end
end
