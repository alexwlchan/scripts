#!/usr/bin/env bash

set -o errexit
set -o nounset

function run_python_tests() {
  
    # In the test suites for flickr.org work, I need a Flickr API key
    # to run certain tests.
    #
    # If I need an API key for my tests, retrieve it from the keychain.
    if grep -rIq 'FLICKR_API_KEY' tests
    then
      export FLICKR_API_KEY=$(keyring get flickr_api key 2>/dev/null)
    fi

    # Run ruff to do Python formatting
    print_info "-> ruff check"
    ruff check .
    
    echo ""
    
    print_info "-> ruff format"
    ruff format .
    
    echo ""
    
    print_info "-> interrogate"
    if ! interrogate
    then
      interrogate -vv
    fi
    
    echo ""

    # This is one repo which is a bit special -- I'm gradually trying to chase
    # the code into `src`, but for now I have to remmeber to look at *.py
    if [[ "$(pwd)" == ~/repos/library-lookup ]]
    then
      print_info '-> mypy *.py src tests'
      mypy *.py src tests
    else
      print_info '-> mypy src tests'
      mypy src tests
    fi
    
    echo ""

    print_info "-> coverage run -m pytest tests"
    coverage run -m pytest tests --quiet
    
    echo ""
    
    print_info "-> coverage report"
    coverage report
}

function run_rust_tests() {
    print_info "-> cargo fmt"
    cargo fmt
    
    echo ""
    
    print_info "-> cargo build"
    cargo build
    
    echo ""
    
    print_info -n "-> cargo test"
    cargo test --quiet
}

if test -f Cargo.toml
then
    run_rust_tests
else
    run_python_tests
fi
