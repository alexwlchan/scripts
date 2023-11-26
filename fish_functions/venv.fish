# Create and activate a new virtualenv.
#
# This is to prevent me from making a very common mistake, which is
# creating the venv and then immediately running "pip install" without
# activating it first.
#
# I upgrade pip because otherwise I get warnings about it being
# out-of-date, and that's annoying.
function new_venv
  python3 -m venv .venv
  source .venv/bin/activate.fish

  python3 -m pip install --upgrade pip

  if [ -f .git ]
    echo .venv >> .git/info/exclude
  end
end
