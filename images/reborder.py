#!/usr/bin/env python3
"""
Adds a white border of consistent width around an image.

I use it when I've taken a screenshot of something on a white background,
and I want to tidy up the crop quickly.
"""

import argparse
import os

from PIL import Image, ImageChops, ImageOps


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("PATH")
    parser.add_argument("BORDER_WIDTH", type=int)
    parser.add_argument("--in-place", action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    im = Image.open(args.PATH)

    bg = Image.new(im.mode, im.size, (255, 255, 255))

    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        im = im.crop(bbox)

    im = ImageOps.expand(im, border=args.BORDER_WIDTH, fill="white")

    name, ext = os.path.splitext(args.PATH)

    if args.in_place:
        out_path = args.PATH
    else:
        out_path = f"{name}.reborder_{args.BORDER_WIDTH}{ext}"

    im.save(out_path)

    print(out_path)
