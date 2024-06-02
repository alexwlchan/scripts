function pyfmt --description "Run Python formatting over a directory"
    if test (count $argv) -eq 0
        set root $PWD
    else
        set root $argv[1]
    end

    ruff check "$root"
    ruff format "$root"
end
