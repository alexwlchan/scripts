#!/usr/bin/env python3
"""
This script creates a 400×400 thumbnail of a specific page of a PDF file.

It uses similar thumbnailing logic to docstore [1], but it allows me to
pick a particular page rather than the first page.

This is helpful because sometimes I download PDF cross-stitch patterns
where the first page contains text which isn't a good thumbnail, but
later pages do show the whole pattern.

[1]: https://github.com/alexwlchan/docstore/blob/main/src/docstore/thumbnails.py

"""

import argparse
import os
import sys
import subprocess
import tempfile

from pypdf import PdfReader, PdfWriter


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Get thumbnails from a specific page of a PDF file.",
    )

    parser.add_argument("PATH")
    parser.add_argument(
        "--page",
        type=int,
        metavar="PAGE_NUMBER",
        help="which page of the PDF to get",
        required=True,
    )
    parser.add_argument(
        "--width", type=int, help="pixel width of the generated thumbnail", default=400
    )

    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    reader = PdfReader(args.PATH)

    # Remember that pages are 0-indexed
    try:
        page = reader.pages[args.page - 1]
    except IndexError:
        sys.exit(f"Unrecognised page: {args.page}, expected 1...{len(reader.pages)}")

    writer = PdfWriter()
    writer.add_page(page)

    with tempfile.TemporaryDirectory(suffix=".pdf") as temp_dir:
        out_path = os.path.join(temp_dir, os.path.basename(args.PATH))

        with open(out_path, "wb") as out_file:
            writer.write(out_file)

        subprocess.check_call(
            ["qlmanage", "-t", out_path, "-s", f"{args.width}x{args.width}", "-o", "."]
        )
