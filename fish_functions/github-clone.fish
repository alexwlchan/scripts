# Clone a GitHub repo given its URL.
#
#     $1 = URL of the GitHub page
#
# Because switching to the repo homepage, clicking, copying the clone URL,
# typing 'git clone', pasting, are all more effort than I care to do manually.
function github-clone --description "Clone a GitHub repository into my ~/repos directory"
    set url "$argv[1]"

    # Get the identifiers for the repository
    set components (string split "/" "$url")

    if [ "$components[3]" != "github.com" ]
        echo "$url is not a GitHub repo"
        return 1
    end

    set owner $components[4]
    set repo $components[5]

    if [ (count $components) -gt 5 ]
        # Detect if this is a pull request, and divert
        if [ $components[6] = pull ]
            github-add-pr-branch "$url"
            return $status
        end
    end

    set repo_url "git@github.com:$owner/$repo.git"

    mkdir -p ~/repos
    cd ~/repos

    if [ -d $repo ]
        # If the repo already exists, check we have the selected fork
        # as a remote.
        cd $repo
        git remote -v | grep "$owner" >/dev/null 2>&1
        if [ $status != 0 ]
            echo "git remote add $owner $repo_url"
            git remote add $owner $repo_url
        end
        set remote (git remote -v | grep "$owner" | awk '{print $1}')
        git fetch
    else
        # Otherwise, clone a fresh copy of the repo
        echo "git clone $repo_url"
        git clone $repo_url
        cd $repo

        # If this looks like a Python repository, create a virtualenv
        # in the root of the repo.
        if [ -f "requirements.txt" ]
            venv
        end

        # I auto-populate .git/info/exclude with a few common entries to
        # save having to do it later.  (I could use a global .gitignore,
        # but this way it's managed programatically and all local to the
        # repo, which I slightly prefer to a homefolder full of manually
        # managed dotfiles.)
        echo .DS_Store >>.git/info/exclude
    end
end

# Given a GitHub pull request, create the repo and make sure the remote
# of the PR owner is added as a remote.
#
#     $1 = URL of the pull request
#
# Sometimes when I'm looking at a pull request, it's useful to get the
# branch locally and test/review/squash it as appropriate.  This makes
# it easier to do so!
#
# Typically not called directly, but detected by 'github-open' and
# switched to if looking at a pull request URL.
function github-add-pr-branch
    # First ensure we have a local clone of the repo
    set url "$argv[1]"
    github-clone (string split "pull/" "$url" | head -n 1)
    if [ $status != 0 ]
        return 1
    end

    # Get the identifiers for the repository.  A pull request URL is
    # of the form
    #
    #     https://github.com/:owner/:repo/pull/:number#discussion_:comment
    #
    set components (string split "/" "$url")

    if [ "$components[6]" != pull ]
        echo "$url is not a GitHub pull request"
        return 1
    end

    set owner $components[4]
    set repo $components[5]
    set number (echo $components[7] | tr '#' ' ' | awk '{print $1}')

    set api_url "https://api.github.com/repos/$owner/$repo/pulls/$number"
    set api_resp (curl -s -H "Accept: application/vnd.github.v3+json" "$api_url")
    set pr_branch (echo $api_resp | jq '.head.repo.full_name' | tr '"' ' ' | awk '{print $1}')

    git checkout (echo $api_resp | jq '.head.ref' | tr '"' ' ' | awk '{print $1}')
end
