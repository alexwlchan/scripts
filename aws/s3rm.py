#!/usr/bin/env python3
"""
A script for deleting all the objects in an S3 prefix.
"""

import argparse
import os
import sys

import humanize
import more_itertools
import tqdm

from _common import create_s3_session, parse_s3_uri
from s3ls import get_objects, get_object_versions

# https://github.com/alexwlchan/concurrently
sys.path.append(os.path.join(os.environ["HOME"], "repos", "concurrently"))

from concurrently import concurrently


def parse_args():
    parser = argparse.ArgumentParser(
        prog="s3rm", description="Delete all the objects in an S3 prefix"
    )

    parser.add_argument("S3_URI")
    parser.add_argument(
        "--with-versions",
        action="store_true",
        help="Delete every version of the objects in S3, not just the latest version",
    )
    parser.add_argument(
        "--start-after", help="Start listing objects at the given key", default=""
    )

    return parser.parse_args()


def delete_objects(sess, iterator):
    total_deleted_count = 0
    total_deleted_size = 0

    def print_result():
        print(f'{humanize.intcomma(total_deleted_count)} object{"s" if total_deleted_count != 1 else ""} deleted, total {humanize.naturalsize(total_deleted_size)}')

    def delete_batch(batch):
        sess.client("s3").delete_objects(
            Bucket=s3_location["Bucket"],
            Delete={
                "Objects": [
                    {k: v for (k, v) in s3_obj.items() if k in {"Key", "VersionId"}}
                    for s3_obj in batch
                ],
            },
        )

    try:
        for batch, _ in concurrently(
            handler=delete_batch,
            inputs=more_itertools.chunked(iterator, 1000)
        ):
            total_deleted_count += len(batch)
            total_deleted_size += sum(s3_obj['Size'] for s3_obj in batch)
    except:
        print_result()
        raise
    else:
        print_result()


if __name__ == "__main__":
    args = parse_args()

    s3_location = parse_s3_uri(args.S3_URI)
    s3_list_args = {"Bucket": s3_location["Bucket"], "Prefix": s3_location["Path"]}

    sess = create_s3_session(args.S3_URI)

    if "--with-versions" in sys.argv:
        iterator = get_object_versions
        s3_list_args["KeyMarker"] = args.start_after
    else:
        iterator = get_objects
        s3_list_args["StartAfter"] = args.start_after

    delete_objects(sess, iterator=tqdm.tqdm(iterator(sess, **s3_list_args)))
