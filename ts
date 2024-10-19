#!/usr/bin/env bash

set -o errexit
set -o nounset

function run_python_tests() {
    export FLICKR_API_KEY=$(keyring get flickr_api key 2>/dev/null)

    ruff check .
    ruff format .

    interrogate -vv

    # This is one repo which is a bit special -- I'm gradually trying to chase
    # the code into `src`, but for now I have to remmeber to look at *.py
    if [[ "$(pwd)" == ~/repos/library-lookup ]]
    then
      mypy *.py src tests
    else
      mypy src tests
    fi

    coverage run -m pytest tests
    coverage report
}

function run_rust_tests() {
    cargo fmt
    cargo build
    cargo test
}

if test -f Cargo.toml
then
    run_rust_tests
else
    run_python_tests
fi
