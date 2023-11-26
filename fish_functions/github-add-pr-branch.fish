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
