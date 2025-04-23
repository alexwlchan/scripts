function add_repo_to_path --description "Add a folder in my ~/repos directory to my PATH"
    set repo_name $argv[1]

    echo "set -g -x PATH ~/repos/$repo_name \"\$PATH\"" >~/.config/fish/conf.d/repos-$repo_name.fish
end
