# text

These are utilities for manipulating streams of text; I consider them in a similar category to Unix staples like <code>head</code> and <code>tail</code>.

## The individual scripts

<dl>
  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/text/midline">
      <code>midline [PATH]</code>
    </a>
  </dt>
  <dd>
    print the line in the middle of a file, e.g. if the file has 5 lines, it prints line 3
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/text/randline">
      <code>randline [NUMBER] < [PATH]</code>
    </a>
  </dt>
  <dd>
    prints randomly selected lines from the given text.
    If `NUMBER` is unspecified, it prints a single line.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/text/reverse">
      <code>reverse < [PATH]</code>
    </a>
  </dt>
  <dd>
    prints the lines of text, but in reverse order.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/text/randline">
      <code>tally < [PATH]</code>
    </a>
  </dt>
  <dd>
    prints a tally of the given text.
  </dd>

  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/text/utf8info">
      <code>echo [STRING] | utf8info</code>
    </a>
  </dt>
  <dd>
    read UTF-8 on stdin and print out the raw Unicode codepoints.
    This is a Docker wrapper around a <a href="https://github.com/lunasorcery/utf8info">tool of the same name</a> by @lunasorcery.
  </dd>
</dl>
