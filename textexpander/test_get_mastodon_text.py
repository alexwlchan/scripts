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
            "A variation on the previous system for todays \#ArtAdventCalendar contribution",
        )
    ],
)
def test_normalise_text(input, output):
    assert normalise_text(input) == output
