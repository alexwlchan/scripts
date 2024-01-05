#!/usr/bin/env python3

import datetime
import os
import subprocess


if __name__ == "__main__":
    latest_download = (
        subprocess.check_output(["/Users/alexwlchan/repos/scripts/fs/latest_download"])
        .strip()
        .decode("utf8")
    )

    name = os.path.basename(latest_download)

    out_dir = os.path.join(
        os.environ["HOME"],
        "textfiles",
        "Attachments",
        str(datetime.datetime.now().year),
    )

    os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, name)

    assert not os.path.exists(out_path)

    os.rename(latest_download, out_path)

    print(f"![[{name}]]")
