import pytest

from save_ao3_links import get_ao3_id


@pytest.mark.parametrize(
    ["url", "ao3_id"],
    [
        ("https://archiveofourown.org/works/1234", "1234"),
        ("https://archiveofourown.org/works/1234?view_adult=true", "1234"),
        (
            "https://archiveofourown.org/works/1234/chapters/5678?view_adult=true",
            "1234",
        ),
    ],
)
def test_get_ao3_id(url, ao3_id):
    assert get_ao3_id(url) == ao3_id
