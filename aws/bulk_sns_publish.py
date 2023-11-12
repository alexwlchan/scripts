#!/usr/bin/env python3
"""
This is a script for bulk publishing messages to SNS.

Suppose I have a large collection of messages I want to send to SNS,
stored as lines in a text file, e.g. some Wellcome catalogue IDs [1].

    xfcrpna3
    qf8sxvxm
    ed3w4fv9
    d4aahw7u
    hwfrryuz

I could loop through the file line-by-line and send them to SNS one-by-one,
but that's slow and inefficient.  It would be more efficient to use the
SNS PublishBatch API to send them ten at a time.

This script provides a convenient wrapper for doing so.

[1]: https://github.com/wellcomecollection/catalogue-pipeline/tree/main/pipeline/id_minter

"""

import argparse
import functools
import itertools
import os
import sys
import uuid

import boto3
import tqdm

from _common import ACCOUNT_NAMES

# https://github.com/alexwlchan/concurrently
sys.path.append(os.path.join(os.environ["HOME"], "repos", "concurrently"))

from concurrently import concurrently  # noqa: E402


def get_aws_session(*, role_arn):
    sts_client = boto3.client("sts")
    assumed_role_object = sts_client.assume_role(
        RoleArn=role_arn, RoleSessionName="AssumeRoleSession1"
    )
    credentials = assumed_role_object["Credentials"]

    return boto3.Session(
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )


def get_session(*, topic_arn):
    """
    Return a boto3 Session for publishing to SNS.

    If it recognises the account which contains the topic, it will pick
    the appropriate IAM role, otherwise it use the default boto3 Session.
    """
    # The arn format of an SNS topic is:
    #
    #       arn:aws:sns:{region}:{account_id}:{topic_name}
    #
    # Extract the account ID.
    account_id = topic_arn.split(":")[4]

    try:
        role_arn = (
            f"arn:aws:iam::{account_id}:role/{ACCOUNT_NAMES[account_id]}-developer"
        )
        return get_aws_session(role_arn=role_arn)
    except KeyError:
        return boto3.Session()


def chunked_iterable(iterable, size):
    """
    Break an iterable into pieces of the given size.

    See https://alexwlchan.net/2018/iterating-in-fixed-size-chunks/
    """
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk


def get_batch_entries(path):
    """
    Given a file which contains one notification per line, generate a series
    of values that can be passed as the `PublishBatchRequestEntries` argument
    to the `Sns.publish_batch` method.
    """
    for batch in chunked_iterable(open(path), size=10):
        yield [{"Id": str(uuid.uuid4()), "Message": line.strip()} for line in batch]


def parse_args():
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Publish lots of notifications to Amazon SNS.",
    )

    parser.add_argument(
        "INPUT_FILE", help="A path containing notifications to send, one per line"
    )
    parser.add_argument(
        "--topic-arn", help="The ARN of the SNS topic to publish to", required=True
    )

    return parser.parse_args()


def publish_batch(sns_client, topic_arn, batch_entries):
    resp = sns_client.publish_batch(
        TopicArn=topic_arn, PublishBatchRequestEntries=batch_entries
    )

    # This is to account for any failures in sending messages to SNS.
    # I've never actually had this happen in practice so I've not written
    # any code to handle it (I'd probably just retry the whole script)
    # but I include it just in case.
    assert len(resp["Failed"]) == 0, resp


def publish_messages(*, input_file, topic_arn):
    sess = get_session(topic_arn=topic_arn)

    # Note: creating boto3 clients isn't thread-safe, so it's important
    # to create it once rather than creating it multiple times in the
    # concurrently() handler.
    #
    # See https://github.com/boto/boto3/issues/801
    sns_client = sess.client("sns")

    total_entries = sum(len(entries) for entries in get_batch_entries(input_file))

    with tqdm.tqdm(total=total_entries) as pbar:
        for batch, _ in concurrently(
            handler=functools.partial(publish_batch, sns_client, topic_arn),
            inputs=get_batch_entries(input_file),
            max_concurrency=8,
        ):
            pbar.update(len(batch))


if __name__ == "__main__":
    args = parse_args()
    publish_messages(input_file=args.INPUT_FILE, topic_arn=args.topic_arn)
