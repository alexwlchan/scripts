#!/usr/bin/env python3
"""
Prepare a cover image for my website, based on an image I've created in Keynote.

You can add the --debug flag to get the intermediate stages saved
as images, so you can see how the script is working.

"""

import collections
import math
import os
import subprocess
import sys

from PIL import Image
import termcolor


def hilight(info):
    return termcolor.colored(info, "blue")


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} [PATH]")

    im = Image.open(path)

    if im.mode != "RGB":
        sys.exit(f"Unsupported image mode: {im.mode}")

    name, ext = os.path.splitext(path)
    ext = ext.replace(".jpeg", ".jpg")

    # Find all the positions with white pixels in the image.
    #
    # This assumes that Keynote may not always get perfectly white, so
    # anything which is almost white is sufficient for these purposes.
    white_pixels = {
        (x, y)
        for x in range(im.width)
        for y in range(im.height)
        if min(im.getpixel((x, y))) >= 250
    }

    if "--debug" in sys.argv:
        im_white = Image.new("RGB", size=im.size)

        for p in white_pixels:
            im_white.putpixel(p, (255, 0, 0))

        im_white.save(f"{name}.debug-1-white_pixels{ext}")

    # Now find all the white "inner corner" pixels -- that is, pixels
    # surrounded on three corners by white pixels, but not the fourth.
    #
    #       wwwwwwwwwww
    #       wCwwwwwwwCw
    #       www......ww
    #       www......ww
    #       www......ww
    #       wCwwwwwwwCw
    #       wwwwwwwwwww
    #
    corner_pixels = set()

    for x, y in white_pixels:
        diagonal = {(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)}
        orthogonal = {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}

        if (
            len(white_pixels.intersection(diagonal)) == 3
            and len(white_pixels.intersection(orthogonal)) == 4
        ):
            corner_pixels.add((x, y))

    if "--debug" in sys.argv:
        im_corner = Image.new("RGB", size=im.size)

        for p in corner_pixels:
            im_corner.putpixel(p, (255, 0, 0))

        im_corner.save(f"{name}.debug-2-corner_pixels{ext}")

    # Group the corners by row.
    #
    # The `corners_by_col` is [x: {y-coords of corners with this y-coord}]
    #
    column_corners = collections.defaultdict(list)

    for x, y in corner_pixels:
        column_corners[x].append(y)

    # Now look for columns with:
    #
    #   1. Exactly two pixels which are corners
    #   2. Another column which has exactly two pixels at the same y-coordinates
    #
    # `rectangles` is [{y-coords}: {x-coords of columns with these y-corners}].
    #
    # This gives us a list of candidate rectangles.
    #
    rectangles = collections.defaultdict(list)

    for x, y_coords in column_corners.items():
        if len(y_coords) == 2:
            rectangles[tuple(sorted(y_coords))].append(x)

    rectangles = {
        y_coords: sorted(x_coords)
        for y_coords, x_coords in rectangles.items()
        if len(x_coords) == 2
    }

    if "--debug" in sys.argv:
        im_corner = Image.new("RGB", size=im.size, color=(255, 255, 255))

        for (y0, y1), (x0, x1) in rectangles.items():
            im_corner.putpixel((x0, y0), (0, 0, 0))
            im_corner.putpixel((x0, y1), (0, 0, 0))
            im_corner.putpixel((x1, y0), (0, 0, 0))
            im_corner.putpixel((x1, y1), (0, 0, 0))

        im_corner.save(f"{name}.debug-3-rectangles{ext}")

    # The outline rectangle is the biggest rectangle; sort by area.
    (y0, y1), (x0, x1) = max(
        rectangles.items(), key=lambda xy: (xy[1][0] - xy[1][1]) * (xy[0][0] - xy[0][1])
    )

    # There may be a little slop here, so slice an extra two pixels off
    # either side to account for light grey pixels that have slipped in.
    # This cropping is only approximate, so this is fine.
    x0 += 2
    y0 += 2
    x1 -= 2
    y1 -= 2

    # Now adjust the pixels so we get a 2:1 aspect ratio in the final image.
    # Again, we don't care about exactness here, slicing a few pixels off
    # either edge is fine.
    width = x1 - x0
    height = y1 - y0

    if height * 2 < width:  # too wide
        diff = width - height * 2
        x0 += int(math.ceil(diff / 2))
        x1 -= int(math.floor(diff / 2))
    elif height * 2 > width:  # too tall
        diff = height * 2 - width
        y0 += int(math.ceil(diff / 2))
        y1 -= int(math.floor(diff / 2))

    # Account for the case where odd/even offsets mean we're actually
    # one away, e.g. 1601 × 800
    if x1 - x0 == (y1 - y0) * 2 + 1:
        x0 += 1

    assert (x1 - x0) == (y1 - y0) * 2

    # Now save the image to an appropriate filename, and tell the user
    cropped_im = im.crop((x0, y0, x1, y1))

    name, ext = os.path.splitext(path)
    ext = ext.replace(".jpeg", ".jpg")
    out_path = f"{name}.cropped{ext}"

    cropped_im.save(out_path, icc_profile=im.info.get("icc_profile"))

    if im.info.get("icc_profile") is not None:
        subprocess.check_call(
            ["srgbify", out_path],
            stdout=subprocess.DEVNULL,
        )

    print(out_path)
    assert cropped_im.width == cropped_im.height * 2
