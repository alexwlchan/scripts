function _run_ruff
    if which ruff >/dev/null
        ruff $argv
    else
        ~/repos/scripts/.venv/bin/ruff $argv
    end
end

function pyfmt --description "Run Python formatting over a directory"
    if test (count $argv) -eq 0
        set root $PWD
    else
        set root $argv[1]
    end

    _run_ruff check "$root"
    _run_ruff format "$root"
end
