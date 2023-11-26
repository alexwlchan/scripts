# Clone a GitHub repo given its URL.
#
#     $1 = URL of the GitHub page
#
# Because switching to the repo homepage, clicking, copying the clone URL,
# typing 'git clone', pasting, are all more effort than I care to do manually.
function github-clone
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
            echo "Creating virtualenv..."
            new_venv
        end

        # I auto-populate .git/info/exclude with a few common entries to
        # save having to do it later.  (I could use a global .gitignore,
        # but this way it's managed programatically and all local to the
        # repo, which I slightly prefer to a homefolder full of manually
        # managed dotfiles.)
        echo .DS_Store >>.git/info/exclude
    end
end
