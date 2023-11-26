# Within a GitHub repository, create a remote named 'alex' for a GitHub fork
# of the same name.  Useful if I cloned before forking.
function gh-add-remote
    set origin_url (git remote get-url origin)
    set repo_name (string split "/" "$origin_url" | tail -n 1)
    git remote add alex "git@github.com:alexwlchan/$repo_name"
end
