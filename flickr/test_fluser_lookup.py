import pytest

from fluser_lookup import get_user_id


@pytest.mark.parametrize(
    ["user_text", "user_id"],
    [
        (
            "https://commons.flickr.org/members/csj_canada_archives/",
            {"path_alias": "csj_canada_archives"},
        ),
    ],
)
def test_get_user_id(user_text, user_id):
    assert get_user_id(user_text) == user_id
