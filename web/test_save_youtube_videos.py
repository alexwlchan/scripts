import pathlib

import pytest

from save_youtube_videos import classify_file_type


@pytest.mark.parametrize(
    ["video_id", "filename", "file_type"],
    [
        ("3VvioE0ziPk", "Who is the loudest sea lion？ [3VvioE0ziPk].mkv", "video"),
        (
            "TE8KMnGm2Xw",
            "Warning, biters ! - A Factorio Short [TE8KMnGm2Xw].webp",
            "thumbnail",
        ),
        ("AfsnHVaScjg", "Ravens can talk! [AfsnHVaScjg].info.json", "info"),
        (
            "IjCylxs8hZU",
            "Soviet Flying Aircraft Carriers Were Ingenious [IjCylxs8hZU].en.vtt",
            "subtitles",
        ),
    ],
)
def test_classify_file_type(video_id, filename, file_type):
    assert classify_file_type(video_id, pathlib.Path(filename)) == file_type
