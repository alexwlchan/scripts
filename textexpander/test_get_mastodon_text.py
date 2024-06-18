import pytest

from get_mastodon_text import normalise_text


@pytest.mark.parametrize(
    ["input", "output"],
    [
        (
            "<p>A variation on the previous system for todays <a "
            'href="https://hachyderm.io/tags/ArtAdventCalendar" class="mention '
            'hashtag" rel="tag">#<span>ArtAdventCalendar</span></a> '
            "contribution</p>",
            "A variation on the previous system for todays \\#ArtAdventCalendar contribution",
        ),
        (
            '<p>my rules for git rebase</p><p>permalink: <a href="https://wizardzines.com/comics/rules-for-rebasing/" rel="nofollow noopener noreferrer" translate="no" target="_blank"><span class="invisible">https://</span><span class="ellipsis">wizardzines.com/comics/rules-f</span><span class="invisible">or-rebasing/</span></a></p>',
            "my rules for git rebase\n\npermalink: https://wizardzines.com/comics/rules-for-rebasing/",
        ),
        (
            "I realize it&#39;s (comparatively) super easy to set up",
            "I realize it's (comparatively) super easy to set up",
        ),
        (
            'The "this site is faster in the app" prompts have the benefit of truth *because they broke the website with React*',
            'The "this site is faster in the app" prompts have the benefit of truth \*because they broke the website with React\*',
        ),
    ],
)
def test_normalise_text(input, output):
    assert normalise_text(input) == output
