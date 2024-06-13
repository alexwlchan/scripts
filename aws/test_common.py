import pytest

from _common import parse_s3_uri


def test_non_s3_uri_is_error():
    with pytest.raises(ValueError, match="Unrecognised scheme"):
        parse_s3_uri(s3_uri="https://www.example.com")


def test_parses_s3_uri():
    assert parse_s3_uri(s3_uri="s3://example-bukkit/my/text/file.txt") == {
        "Bucket": "example-bukkit",
        "Path": "my/text/file.txt",
    }
