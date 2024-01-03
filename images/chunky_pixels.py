#!/usr/bin/env python3
"""
Redraws the given image with 'chunky pixels' – every NxN chunk of pixels
is replaced by a single colour.
"""

import colorsys
import random
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw
import tqdm


def clamp(x, *, between):
    lower, upper = between
    return min([max([x, lower]), upper])


if __name__ == "__main__":
    try:
        path = sys.argv[1]
        pixel_size = int(sys.argv[2])
    except (IndexError, ValueError):
        sys.exit(f"Usage: {__file__} <PATH> <PIXEL_SIZE>")

    im = Image.open(path)

    assert im.width % pixel_size == 0
    assert im.height % pixel_size == 0

    all_colours = {}

    with tempfile.TemporaryDirectory() as tmpdir:
        for x_start in tqdm.tqdm(range(0, im.width, pixel_size)):
            for y_start in range(0, im.height, pixel_size):
                im_crop = im.crop(
                    (x_start, y_start, x_start + pixel_size, y_start + pixel_size)
                )
                tmp_path = f"{tmpdir}/cropped_{x_start}_{y_start}.png"
                im_crop.save(tmp_path)
                colour = subprocess.check_output(
                    ["dominant_colours", tmp_path, "--max-colours=1", "--no-palette"]
                ).strip()
                all_colours[(x_start, y_start)] = (
                    int(colour[1:3], 16),
                    int(colour[3:5], 16),
                    int(colour[5:7], 16),
                )

    im = Image.new("RGB", im.size)
    draw = ImageDraw.Draw(im)

    for (x_start, y_start), (r, g, b) in all_colours.items():
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        l = clamp(l * random.uniform(0.9, 1.1), between=[0, 1])
        s = clamp(s * random.uniform(0.9, 1.1), between=[0, 1])

        r, g, b = colorsys.hls_to_rgb(h, l, s)
        draw.rectangle(
            [(x_start, y_start), (x_start + pixel_size), (y_start + pixel_size)],
            fill=(int(r * 255), int(g * 255), int(b * 255)),
        )

    base, extension = path.rsplit(".", 1)

    out_path = f"{base}_{pixel_size}.{extension}"
    im.save(out_path)
