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

"""

import argparse
import collections
import datetime
import os
import sys
from typing import List

import attr
import boto3
import humanize
import natsort
import termcolor

from _common import create_s3_session, parse_s3_uri


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


def create_link_text(*, url, label):
    # Based on https://stackoverflow.com/a/71309268/1558022

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
    return f"\033]8;;{url}\033\\{label}\033]8;;\033\\"


def pprint_nested_tree(bucket, tree, folder_counts, parents=None):
    lines = []
    parents = parents or []

    if not parents:
        lines.append(".")

    entries = sorted(tree.items())

    for i, (key, nested_tree) in enumerate(entries, start=1):
        if parents:
            full_path = f'{"/".join(parents)}/{key}'
        else:
            full_path = key
        if isinstance(key, str):
            label = create_link_text(
                url=f"https://eu-west-1.console.aws.amazon.com/s3/buckets/{bucket}?prefix={full_path}/&showversions=false",
                label=f"{key}/",
            )
        else:
            label = key

        if full_path in folder_counts:
            obj_count_line = termcolor.colored(
                f"...plus {folder_counts[full_path]} object{'s' if folder_counts[full_path] > 1 else ''}",
                "blue",
            )

            if i == len(entries) and nested_tree:
                obj_count_line = f"    ├── {obj_count_line}"
            elif i == len(entries):
                obj_count_line = f"    └── {obj_count_line}"
            elif nested_tree:
                obj_count_line = f"│   ├── {obj_count_line}"
            else:
                obj_count_line = f"│   └── {obj_count_line}"
        else:
            obj_count_line = None

        if i == len(entries):
            lines.append("└── " + label)

            if obj_count_line is not None:
                lines.append(obj_count_line)

            lines.extend(
                [
                    "    " + l
                    for l in pprint_nested_tree(
                        bucket,
                        nested_tree,
                        folder_counts=folder_counts,
                        parents=parents + [key],
                    )
                ]
            )
        else:
            lines.append("├── " + label)

            if obj_count_line is not None:
                lines.append(obj_count_line)

            lines.extend(
                [
                    "│   " + l
                    for l in pprint_nested_tree(
                        bucket,
                        nested_tree,
                        folder_counts=folder_counts,
                        parents=parents + [key],
                    )
                ]
            )

    return lines


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

        extra_objects = f"...{len(tree.objects) - 3} other objects"
        lines.append(f"{prefix_char} {termcolor.colored(extra_objects, 'blue')}")

    for i, (folder_name, folder_tree) in enumerate(
        sorted(tree.folders.items()), start=1
    ):
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

    s3_prefix = parse_s3_uri(args.S3_URI)

    sess = create_s3_session(args.S3_URI)

    s3_objects = list(list_s3_objects(sess, **s3_prefix))

    if not s3_objects:
        print("(no objects)")
        sys.exit(1)

    keys = [s3_obj["Key"] for s3_obj in s3_objects if s3_obj["Size"] > 0]

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
        last_modified_message = last_modified.strftime("%d %B")

    print(
        termcolor.colored(
            f'{humanize.intcomma(len(s3_objects))} object{"s" if len(s3_objects) > 1 else ""}, '
            f"totalling {humanize.naturalsize(total_size)}, "
            f"last modified {last_modified_message}",
            "green",
        )
    )
