import pytest

from fluser_lookup import get_user_id


@pytest.mark.parametrize(
    ["user_text", "user_id"],
    [
        (
            "https://commons.flickr.org/members/csj_canada_archives/",
            {"path_alias": "csj_canada_archives"},
        ),
        (
            "https://www.flickr.com/photos/powerhouse_museum/2532449275/",
            {"path_alias": "powerhouse_museum"},
        ),
        (
            "https://www.flickr.com/people/alexwlchan/",
            {"path_alias": "alexwlchan"},
        ),
        (
            "35468159852@N01",
            {"id": "35468159852@N01"},
        ),
        (
            "https://www.flickr.com/photos/35468159852@N01/",
            {"id": "35468159852@N01"},
        ),
    ],
)
def test_get_user_id(user_text, user_id):
    assert get_user_id(user_text) == user_id
