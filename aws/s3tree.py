#!/usr/bin/env python3
"""
Prints a tree showing the structure of an S3 prefix.

This is meant to give me an overview of what's in a prefix, not
a complete listing.  Here's an example of what the output looks like:

    .
    └─ digitised/
        └─ b12840889/
            └─ v1/
                ├─ bag-info.txt
                ├─ bagit.txt
                ├─ manifest-sha256.txt
                ├─ tagmanifest-sha256.txt
                └─ data/
                    ├─ b12840889.xml
                    ├─ b12840889_0001.xml
                    └─ objects/
                        ├─ b12840889_0001_0001.jp2
                        ├─ b12840889_0001_0002.jp2
                        ├─ b12840889_0001_0003.jp2
                        └─ ...2785 other objects

The folder names link to the S3 console, so I can jump into exploring the
objects in more detail if useful.

== Interesting features ==

*   It tries to pick an appropriate IAM role based on the bucket name
    (this only works for some buckets, and ones I have access to).

*   The folder names are all clickable links that go to the S3 console,
    so I can jump into more detailed inspection.

*   It does natural sorting of S3 keys rather than alphabetical, which is
    useful when I have lots of numeric-esque keys like in the example.

"""

import argparse
import collections
import datetime
import sys
from typing import List

import attr
import humanize
import natsort
import termcolor

from _common import create_link_text, create_s3_session, parse_s3_uri


def parse_args():
    parser = argparse.ArgumentParser(
        prog="s3tree", description="Print a summary tree of an S3 prefix"
    )

    parser.add_argument("S3_URI")

    return parser.parse_args()


def list_s3_objects(sess, **kwargs):
    s3 = sess.client("s3")

    for page in s3.get_paginator("list_objects_v2").paginate(**kwargs):
        yield from page.get("Contents", [])


@attr.s
class S3Folder:
    path: str = attr.ib()
    objects: List[str] = attr.ib(factory=list)
    folders = attr.ib(factory=dict)  # Mapping[str, S3Folder]


def build_s3_tree(keys, path=None):
    path = path or []

    tree = S3Folder(path="/".join(path))

    per_folder_keys = collections.defaultdict(list)

    for k in keys:
        if "/" in k:
            folder_name, entry_name = k.split("/", 1)
            per_folder_keys[folder_name].append(entry_name)
        else:
            per_folder_keys["."].append(k)

    assert sum(len(entries) for entries in per_folder_keys.values()) == len(keys)

    tree.objects = natsort.natsort(per_folder_keys.pop(".", []))

    for folder_name, folder_keys in per_folder_keys.items():
        tree.folders[folder_name] = build_s3_tree(
            folder_keys, path=path + [folder_name]
        )

    return tree


def pprint_s3tree(*, bucket, tree):
    lines = []

    # If we're at the top of the tree, we want to print a '.'
    if tree.path == "":
        lines.append(".")

    # Start by printing any objects that are in this folder.  Print up to
    # 4 objects, otherwise print 3 and then '...X other objects'
    if len(tree.objects) == 4:
        tree_object_count = 4
    else:
        tree_object_count = 3

    for i, object_key in enumerate(sorted(tree.objects[:tree_object_count]), start=1):
        if tree.folders or len(tree.objects) > i:
            prefix_char = "├─"
        else:
            prefix_char = "└─"

        lines.append(f"{prefix_char} {termcolor.colored(object_key, 'blue')}")

    if len(tree.objects) > tree_object_count:
        if tree.folders:
            prefix_char = "├─"
        else:
            prefix_char = "└─"

        # if there's only one more object left in the folder, we should
        # just print it rather than '...1 other object'
        assert len(tree.objects) - 3 > 1

        extra_objects = f"...{len(tree.objects) - 3} other objects"
        lines.append(f"{prefix_char} {termcolor.colored(extra_objects, 'blue')}")

    for i, folder_name in enumerate(natsort.natsort(tree.folders), start=1):
        folder_tree = tree.folders[folder_name]

        if tree.path == "":
            full_path = folder_name
        else:
            full_path = "/".join([tree.path, folder_name])

        if len(tree.folders) > i:
            folder_prefix_char = "├─"
            sub_prefix_char = "│   "
        else:
            folder_prefix_char = "└─"
            sub_prefix_char = "    "

        lines.append(
            folder_prefix_char
            + " "
            + create_link_text(
                url=f"https://eu-west-1.console.aws.amazon.com/s3/buckets/{bucket}?prefix={full_path}/&showversions=false",
                label=f"{folder_name}/",
            )
        )
        lines.extend(
            [
                f"{sub_prefix_char}{ln}"
                for ln in pprint_s3tree(bucket=bucket, tree=folder_tree)
            ]
        )

    return lines


if __name__ == "__main__":
    args = parse_args()

    s3_location = parse_s3_uri(args.S3_URI)
    s3_prefix = {"Bucket": s3_location["Bucket"], "Prefix": s3_location["Path"]}

    sess = create_s3_session(args.S3_URI)

    s3_objects = list(list_s3_objects(sess, **s3_prefix))

    if not s3_objects:
        print("(no objects)")
        sys.exit(1)

    keys = [
        s3_obj["Key"]
        for s3_obj in s3_objects
        if s3_obj["Size"] > 0 or not s3_obj["Key"].endswith("/")
    ]

    tree = build_s3_tree(keys)

    print("\n".join(pprint_s3tree(bucket=s3_prefix["Bucket"], tree=tree)))

    print("")
    total_size = sum(s3_obj["Size"] for s3_obj in s3_objects)
    last_modified = max(s3_obj["LastModified"] for s3_obj in s3_objects)

    if last_modified.date() == datetime.date.today():
        last_modified_message = "today"
    elif last_modified.year != datetime.date.today().year:
        last_modified_message = f"in {last_modified.strftime('%B %Y')}"
    else:
        last_modified_message = last_modified.strftime("%-d %B")

    print(
        termcolor.colored(
            f"{humanize.intcomma(len(s3_objects))} object{'s' if len(s3_objects) > 1 else ''}, "
            f"totalling {humanize.naturalsize(total_size)}, "
            f"last modified {last_modified_message}",
            "green",
        )
    )
