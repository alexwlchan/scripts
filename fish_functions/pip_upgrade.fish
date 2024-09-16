function pip_upgrade --description "Upgrade requirements.txt lock files with uv"
    if test \( -e requirements.in \) -a \( -e overrides.txt \)
        uv pip compile requirements.in --output-file requirements.txt --override overrides.txt --upgrade
    else if test \( -e requirements.in \)
        uv pip compile requirements.in --output-file requirements.txt --upgrade
    end

    if test \( -e dev_requirements.in \) -a \( -e overrides.txt \)
        uv pip compile dev_requirements.in --output-file dev_requirements.txt --override overrides.txt --upgrade
    else if test \( -e dev_requirements.in \)
        uv pip compile dev_requirements.in --output-file dev_requirements.txt --upgrade
    end
end
