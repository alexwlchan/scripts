#!/usr/bin/env python3
"""
Get the checksum/hash of an object in S3.
"""

import argparse
import hashlib
import os

from _common import create_link_text, create_s3_session, parse_s3_uri


def parse_args():
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__), description="Get the hash of an object in S3"
    )

    parser.add_argument("S3_URI")
    parser.add_argument(
        "--algorithm", help="which checksum algorithm to use", default="sha256"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    s3_location = parse_s3_uri(args.S3_URI)

    sess = create_s3_session(args.S3_URI)

    s3_obj = sess.client("s3").get_object(
        Bucket=s3_location["Bucket"], Key=s3_location["Path"]
    )

    h = hashlib.new(args.algorithm)

    while chunk := s3_obj["Body"].read(8192):
        h.update(chunk)

    print(h.hexdigest(), end="")
