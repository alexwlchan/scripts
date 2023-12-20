#!/usr/bin/env python3
"""
This script takes a PDF, and creates a new PDF with just the images
filling the page.

It's working around a behaviour of the "Scan Document" feature in the
iOS Notes app – when you export the scan as PDF, it adds large white
borders around the images which is precisely what I don't want.
"""

import sys

from pypdf import PdfReader


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <PATH>")

    reader = PdfReader(path)

    images = []

    for page in reader.pages:
        images.extend([im.image for im in page.images])

    assert len(images) == len(reader.pages)

    images[0].save(
        path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )
