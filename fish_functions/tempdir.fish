function tmpdir --description "Quickly create and switch into a temporary directory"
    cd (mktemp -d)
end
