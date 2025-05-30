#!/usr/bin/env python3
"""
This is a script for creating colour-tinted versions of greyscale images.

It works by creating an RGBA image which has the specified colour
on every pixel, then controlling the intensity with the alpha value.

I don't use it especially often, but I thought it was a neat trick and
I wanted to save it for future use.
"""

import sys

from PIL import Image


if __name__ == "__main__":
    try:
        path = sys.argv[1]
        hex_colour = sys.argv[2]
    except IndexError:
        sys.exit(f"Usage: {__file__} <PATH> <HEX_COLOUR>")

    red = int(hex_colour[1:3], 16)
    green = int(hex_colour[3:5], 16)
    blue = int(hex_colour[5:7], 16)

    im = Image.open(path)
    im = im.convert("L")
    pixels = list(im.getdata())
    tinted_im = Image.new("RGBA", im.size)

    if im.mode == "L":
        tinted_im.putdata([(red, green, blue, 255 - p) for p in pixels])
    else:
        tinted_im.putdata([(red, green, blue, 255 - p[0]) for p in pixels])

    name, _ = path.rsplit(".", 1)
    out_path = f"{name}.{hex_colour.strip('#')}.png"

    tinted_im.save(out_path)
    print(out_path)
