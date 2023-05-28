# python

These scripts are all related to [Python], a scripting language I use a lot of (including in the rest of this repo!).

[Python]: https://www.python.org/

## The individual scripts

<dl>
  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/python/pip_freeze">
      <code>pip_freeze [FILE]</code>
    </a>
  </dt>
  <dd>
    this tries to add a comment to any imports I have in a file, telling me what version I had installed when I wrote a script, e.g.
    <pre><code>import os
import humanize</code></pre>
becomes
    <pre><code>import os
import humanize  # humanize==4.4.0</code></pre>
    I use it for lightweight dependency tracking, when I have a script that I don’t want to write an entire <code>requirements.txt</code> file for.
  </dd>
</dl>
