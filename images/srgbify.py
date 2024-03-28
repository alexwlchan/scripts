#!/usr/bin/env python3
"""
A script that converts images to an sRGB colour profile.

This is particularly useful for screenshots on macOS, which are taken
with the display's colour profile (e.g. Display LCD or Display P3), but
which I want to convert to sRGB for converting on the web.

Note: this is a potentially destructive script.  Don't run this on images
you care about if you don't have a backup!

*   It overwrites the original image file.
*   It strips out EXIF metadata.

Based on https://github.com/python-pillow/Pillow/issues/1662
"""

import io
import sys
import typing

from PIL import Image, ImageCms, ImageOps
from PIL.ImageCms import PyCMSError
from pillow_heif import register_heif_opener


register_heif_opener()


def convert_image_to_srgb(im: Image) -> typing.Union[Image, None]:
    """
    Convert an image to sRGB and return a new Image instance.
    """
    icc_profile = im.info.get("icc_profile")

    # If this image doesn't have a colour profile, we're done.
    if icc_profile is None:
        return None

    # If the image has an EXIF orientation tag, it will be stripped out
    # upon saving (like all EXIF metadata).
    #
    # To avoid any weird rotation issues, bake the rotation into the image.
    # See https://github.com/python-pillow/Pillow/issues/4703#issuecomment-645219973
    # or the associated test.
    #
    # See https://github.com/alexwlchan/scripts/issues/21
    im = ImageOps.exif_transpose(im)

    # Otherwise, convert the image to an sRGB colour profile and return that.
    try:
        return ImageCms.profileToProfile(
            im,
            inputProfile=io.BytesIO(icc_profile),
            outputProfile=ImageCms.createProfile("sRGB"),
        )
    except PyCMSError as err:
        if (
            im.mode == "L"
            and b"GRAYXYZ" in icc_profile
            and err.args[0].args == ("cannot build transform",)
        ):
            return ImageCms.profileToProfile(
                im,
                inputProfile=io.BytesIO(icc_profile),
                outputProfile=ImageCms.createProfile("sRGB"),
                outputMode="RGB",
            )
        else:
            raise

    return out_im


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit(f"Usage: {__file__} <PATH...>")

    for path in sys.argv[1:]:
        im = Image.open(path)
        out_im = convert_image_to_srgb(im)

        if out_im is not None:
            out_im.save(path)

        print(path)
