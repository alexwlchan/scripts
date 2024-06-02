function pip_sync --description "Make a virtualenv dependencies look like requirements.txt"
    pip_compile

    if test \( -e dev_requirements.txt \)
        uv pip sync dev_requirements.txt
    else if test \( -e requirements.txt \)
        uv pip sync requirements.txt
    end
end
