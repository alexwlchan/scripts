function reload_fish_config
    source ~/.config/fish/config.fish

    for file in $conf_dir/*.fish
        source "$file"
    end
    
    for file in ~/repos/scripts/fish_functions/*.fish
        source "$file"
    end
end
