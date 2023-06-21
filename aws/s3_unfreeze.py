#!/usr/bin/env python3
"""
This is a rudimentary script for restoring S3 objects from Glacier.

You pass it a text file with a list of S3 URIs to restore, and it will
initiate a Glacier restore for each of them.

You can also use it to track the progress of a restore operation -- it
reports a count of how many objects are in-progress/already restored.
"""

import os
import sys

from botocore.exceptions import ClientError
import hyperlink
import tqdm

from _common import create_s3_session

sys.path.append(os.path.join(os.environ["HOME"], "repos", "concurrently"))
from concurrently import concurrently


def restore_object(s3_client, s3_uri):
    uri = hyperlink.URL.from_text(s3_uri)

    bucket = uri.host
    key = "/".join(uri.path)

    head_resp = s3_client.head_object(Bucket=bucket, Key=key)

    if head_resp.get('Restore') == 'ongoing-request="true"':
        return "RestoreInProgress"

    if 'ongoing-request="false"' in head_resp.get('Restore', ''):
        return 'RestoredSuccessfully'

    try:
        resp = s3_client.restore_object(
            Bucket=bucket,
            Key=key,
            RestoreRequest={"Days": 7, "GlacierJobParameters": {"Tier": "Standard"}},
        )
    except ClientError as err:
        if err.response["Error"]["Code"] == "RestoreAlreadyInProgress":
            return "RestoreInProgress"
        else:
            raise

    if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return "RestoredSuccessfully"
    else:
        return "RestoreInProgress"


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <LIST_OF_KEYS>")

    results = {
        "RestoredSuccessfully": 0,
        "RestoreInProgress": 0,
    }

    with open(path) as infile:
        s3_uris = [line.strip() for line in infile]

    s3 = create_s3_session(s3_uris[0], role_name="developer").client("s3")

    for _, output in tqdm.tqdm(
        concurrently(inputs=s3_uris, handler=lambda s3_uri: restore_object(s3, s3_uri)),
        total=len(s3_uris),
    ):
        results[output] += 1

    from pprint import pprint

    pprint(results)
