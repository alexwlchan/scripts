function pyfmt --description "Run Python formatting over a directory"
    if test (count $argv) -eq 0
        set root $PWD
    else
        set root $argv[1]
    end

    black "$root"

    # E501 = line too long; anything up to 100-ish is fine in my book
    # (the "ish" is intentional; see https://www.youtube.com/watch?v=wf-BqAjZb8M)
    #
    # E203/W503/W504 = this is where black and flake8 conflict, see https://black.readthedocs.io/en/stable/faq.html#why-are-flake8-s-e203-and-w503-violated
    flake8 \
        --ignore=E501,E203,W503 --extend-select=W504 \
        --exclude .venv \
        "$root"
end
