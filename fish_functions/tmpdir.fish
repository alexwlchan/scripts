function tmpdir --description "Create and switch into a temporary directory"
    cd (mktemp -d)
end
