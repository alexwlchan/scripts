#!/usr/bin/env bash

set -o errexit
set -o nounset

function run_python_tests() {
    REPO_NAME="$(basename $(pwd))"
  
    # In the test suites for flickr.org work, I need a Flickr API key
    # to run certain tests.
    #
    # If I need an API key for my tests, retrieve it from the keychain.
    if [[ "$REPO_NAME" = "commons.flickr.org" ]]
    then
        print_info 'export FLICKR_API_KEY=$(keyring get flickr_api key)'
        export FLICKR_API_KEY=$(keyring get flickr_api key)
        
        echo ""
    elif [[ "$REPO_NAME" = "data-lifeboat" ]]
    then
        print_info 'export FLICKR_API_KEY=$(keyring get data_lifeboat_creator flickr_client_key)'
        export FLICKR_API_KEY=$(keyring get data_lifeboat_creator flickr_client_key)
        
        echo ""
    fi

    # Run ruff to do Python formatting
    if [[ "${1:-}" == "--fix" ]]
    then
        print_info "-> ruff check --fix"
        ruff check --fix .
    else
        print_info "-> ruff check"
        ruff check .
    fi
    
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
    if [[ "$REPO_NAME" = "library-lookup" ]]
    then
        print_info '-> mypy *.py src tests'
        mypy *.py src tests
    else
        print_info '-> mypy src tests'
      
        if mypy src tests >/dev/null
        then
            mypy src tests --no-color-output
        else
            mypy src tests
        fi
    fi
    
    echo ""

    # Run the tests.
    #
    # I have a couple of repos which are a bit special and need a
    # different command because I use pytest-xdist, but not all
    # my repos work that way.
    if [[ "$REPO_NAME" = "commons.flickr.org" ]]
    then
        print_info "-> pytest tests/ --ignore uptime_tests/ --quiet"
        pytest --cov=src --cov=tests tests --ignore uptime_tests --quiet
    elif [[ "$REPO_NAME" = "data-lifeboat" ]] ||
         [[ "$REPO_NAME" = "flickr-photos-api" ]] ||
         [[ "$REPO_NAME" = "analytics.alexwlchan.net" ]]
    then
        print_info "-> pytest tests --no-cov"
        pytest tests/ --quiet --no-cov
    else
        print_info "-> coverage run -m pytest tests"
        coverage run -m pytest tests --quiet
    fi
    
    echo ""

    print_info "-> coverage report"

    if [[ $(coverage report --format=total) = "100" ]]
    then
        echo "100% coverage!"
    else
        coverage report
    fi
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
    run_python_tests "$@"
fi
