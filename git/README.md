# git

These scripts are all shortcuts for using [Git], mostly designed to let me do my common Git tasks with as little typing as possible.

[Git]: https://git-scm.com/

## The individual scripts

<dl>
  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/git/bad">
      <code>bad</code>
    </a> / <a href="https://github.com/alexwlchan/scripts/blob/main/git/good">
      <code>good</code>
    </a>
  </dt>
  <dd>
    alias for <a href="https://git-scm.com/docs/git-bisect"><code>git bisect bad / good</code></a>
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/git/cleanup_branches">
      <code>cleanup_branches</code>
    </a>
  </dt>
  <dd>
    clean up any local branches which have been merged into the primary branch (<code>main</code>, <code>master</code>, etc.)
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/git/find_big_commits">
      <code>find_big_commits</code>
    </a>
  </dt>
  <dd>
    print some information about the biggest files/commits in the Git history.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/git/gb">
      <code>gb [name]</code>
    </a>
  </dt>
  <dd>
    alias for <a href="https://git-scm.com/docs/git-checkout"><code>git checkout -b [name]</code></a>, which creates a new branch
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/git/gc">
      <code>gc [name]</code>
    </a>
  </dt>
  <dd>
    alias for <a href="https://git-scm.com/docs/git-checkout"><code>git checkout</code></a>, which switches to the given branch
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/git/gcb">
      <code>gcb</code>
    </a>
  </dt>
  <dd>
    <strong>g</strong>et the name of the <strong>c</strong>urrent <strong>b</strong>ranch
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/git/gf">
      <code>gf</code>
    </a>
  </dt>
  <dd>
    alias for <a href="https://git-scm.com/docs/git-checkout"><code>git fetch origin --prune</code></a>, which gets updated information about all the branches on the remote server
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/git/gitstats">
      <code>gitstats</code>
    </a>
  </dt>
  <dd>
    print a brief line count summary of my local Git changes (any staged and uncommitted changes)
    <p>
    <pre><code>$ gitstats
+++  0 additions
--- 57 deletions</code></pre>
    </p>
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/git/gm">
      <code>gm</code>
    </a>
  </dt>
  <dd>
    switch to the primary branch (usually <code>main</code>, hence <code>gm</code>) and pull any changes from the remote server
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/git/gp">
      <code>gp</code>
    </a>
  </dt>
  <dd>
    <strong>p</strong>ull any changes on the current branch from the remote server
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/git/groot">
      <code>groot</code>
    </a>
  </dt>
  <dd>
    alias for <code>git rev-parse --show-toplevel</code>, which prints the root of the current repository
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/git/gub">
      <code>gub</code>
    </a>
  </dt>
  <dd>
    open the current Git repo in my web browser (assuming it's a GitHub repo)
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/git/gup">
      <code>gup</code>
    </a>
  </dt>
  <dd>
    open the current Git repo in <a href="https://gitup.co/">GitUp</a>, my GUI Git client of choice
  </dd>
</dl>
