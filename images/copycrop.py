#!/usr/bin/env python3
"""
This "copies" the crop of one image pair to another.

Suppose we have a pair of images, one which has been cropped from
the other:

    +----------+
    |x.x.111.x.|                +-----+
    |.x.x.x.x.x|      --->      |x.111|
    |x.x.x.x.x.|                +-----+
    +----------+

This script will identify where the cropped image came from the
bigger image, then apply that crop to a second image which has the
same dimensions:

    +----------+
    |.y.y222.y.|                +-----+
    |y.y.y.y.y.|      --->      |y222.|
    |.y.y.y.y.y|                +-----+
    +----------+

This is a very rudimentary form of "template matching" [1].  It relies
on the first pair of images being only a crop, and not modified in any
other way.  This is the case for images I've made (screenshots), but
it may fail if the image has been processed in other ways.

See the README for a more visual example.

[1]: https://en.wikipedia.org/wiki/Template_matching

"""

import argparse
import collections
import itertools
import os

from PIL import Image
from PIL import ImageChops


def parse_args():
    parser = argparse.ArgumentParser(
        prog="copycrop", description="Copy the crop from one image to another"
    )

    parser.add_argument("ORIGINAL_IMAGE_1")
    parser.add_argument("CROPPED_IMAGE_1")
    parser.add_argument("ORIGINAL_IMAGE_2")

    return parser.parse_args()


def find_crop_region(original: Image, cropped: Image):
    """
    Given the pair of images, work out where the cropped image appears
    in the original.

    This returns a 4-tuple (left, top, right, bottom) which can be passed
    into the Image.crop method, e.g. (990, 332, 1864, 677).

    == How it works ==

    We look at the palette of both images, and in particular colours which
    appear in both.  Then we compare their relative positions, and use them
    to "guess" some possible candidates for the crop.

    e.g. if there's a single red pixel in both images, which:

    * appears at (10, 10) in the original image
    * appears at (1, 1) in the cropped image

    then we can guess this is the same red pixel, and try a crop that
    starts at (10, 10).

    """
    original_palette = collections.Counter(original.getdata())
    cropped_palette = collections.Counter(cropped.getdata())

    least_frequent_colour = min(
        cropped_palette, key=lambda c: original_palette[c] * cropped_palette[c]
    )

    original_pixels = original.load()

    matching_original_coordinates = {
        (x, y)
        for x in range(original.width)
        for y in range(original.height)
        if original_pixels[x, y] == least_frequent_colour
    }

    cropped_pixels = cropped.load()

    matching_crop_coordinates = {
        (x, y)
        for x in range(cropped.width)
        for y in range(cropped.height)
        if cropped_pixels[x, y] == least_frequent_colour
    }

    for (original_x, original_y), (cropped_x, cropped_y) in itertools.product(
        matching_original_coordinates, matching_crop_coordinates
    ):
        left = original_x - cropped_x
        top = original_y - cropped_y

        crop_info = (
            left,
            top,
            left + cropped.width,
            top + cropped.height,
        )

        new_crop = original.crop(crop_info)

        diff = ImageChops.difference(cropped, new_crop)
        if diff.getbbox() is None:
            return crop_info

    raise RuntimeError("Could not find cropped image inside original image!")


if __name__ == "__main__":
    args = parse_args()

    original_im_1 = Image.open(args.ORIGINAL_IMAGE_1)
    original_im_2 = Image.open(args.ORIGINAL_IMAGE_2)

    if original_im_1.size != original_im_2.size:
        raise ValueError("Original images must have the same dimensions!")

    cropped_im_1 = Image.open(args.CROPPED_IMAGE_1)

    crop_region = find_crop_region(original_im_1, cropped_im_1)

    cropped_im_2 = original_im_2.crop(crop_region)

    name, ext = os.path.splitext(args.ORIGINAL_IMAGE_2)
    out_path = f"{name}.cropped.{ext}"
    cropped_im_2.save(out_path)
    print(out_path)
