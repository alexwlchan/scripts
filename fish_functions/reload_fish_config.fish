function reload_fish_config --description "Load the latest version of my fish config"
    source ~/.config/fish/config.fish

    for file in ~/.config/fish/conf.d/*.fish
        source "$file"
    end

    for file in ~/repos/scripts/fish_functions/*.fish
        source "$file"
    end
end
