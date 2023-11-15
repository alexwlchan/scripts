#!/usr/bin/env python3
"""
A script that converts images to an sRGB colour profile.

This is particularly useful for screenshots on macOS, which are taken
with the display's colour profile (e.g. Display LCD or Display P3), but
which I want to convert to sRGB for converting on the web.

Based on https://github.com/python-pillow/Pillow/issues/1662
"""

import sys
import tempfile

from PIL import Image, ImageCms


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit(f"Usage: {__file__} <PATH...>")

    for path in sys.argv[1:]:
        in_img = Image.open(path)

        srgb_profile = ImageCms.createProfile("sRGB")

        icc_profile = in_img.info.get("icc_profile")

        # Handle the case where this image doesn't have
        # a colour profile
        if icc_profile is None:
            print(path)
            continue

        _, icc_profile_path = tempfile.mkstemp(suffix=".icc")

        with open(icc_profile_path, "wb") as out_file:
            out_file.write(icc_profile)

        out_img = ImageCms.profileToProfile(
            in_img, inputProfile=icc_profile_path, outputProfile=srgb_profile
        )

        out_img.save(path)
        print(path)
