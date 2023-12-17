import pytest

from fix_twitter_thread import fix_emoji, remove_profile_links


@pytest.mark.parametrize(
    ["input", "output"],
    [
        ("![✍🏻](https://abs-0.twimg.com/emoji/v2/svg/270d-1f3fb.svg)", "✍🏻"),
        (
            '![✍🏻](https://abs-0.twimg.com/emoji/v2/svg/270d-1f3fb.svg)![📚](https://abs-0.twimg.com/emoji/v2/svg/1f4da.svg "Books")',
            "✍🏻📚",
        ),
    ],
)
def test_fix_emoji(input: str, output: str) -> None:
    assert fix_emoji(input) == output


def test_remove_profile_links() -> None:
    assert (
        remove_profile_links(
            "[Elle McNicoll ✍🏻📚](https://twitter.com/BooksandChokers) \n",
            handle="BooksandChokers",
        )
        == ""
    )
