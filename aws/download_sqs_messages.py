#!/usr/bin/env python3

import json
import sys

import boto3
import tqdm

from _common import ACCOUNT_NAMES, get_aws_session


def list_queue_urls():
    sess = boto3.Session()
    paginator = sess.client("sqs").get_paginator("list_queues")

    for page in paginator.paginate():
        yield from page["QueueUrls"]


def get_session(*, queue_url):
    """
    Return a boto3 Session for publishing to SNS.

    If it recognises the account which contains the queue, it will pick
    the appropriate IAM role, otherwise it use the default boto3 Session.
    """
    # The arn format of an SQS queue URL is:
    #
    #       https://sqs.eu-west-1.amazonaws.com/1234567890/queue-name
    #
    # Extract the account ID.
    account_id = queue_url.split("/")[3]

    try:
        role_arn = (
            f"arn:aws:iam::{account_id}:role/{ACCOUNT_NAMES[account_id]}-developer"
        )
        return get_aws_session(role_arn=role_arn)
    except KeyError:
        return boto3.Session()


def download_messages(*, queue_url):
    sess = get_session(queue_url=queue_url)

    sqs_client = sess.client("sqs")

    while True:
        resp = sqs_client.receive_message(
            QueueUrl=queue_url, AttributeNames=["All"], MaxNumberOfMessages=10
        )

        try:
            yield from resp["Messages"]
        except KeyError:
            return

        entries = [
            {"Id": msg["MessageId"], "ReceiptHandle": msg["ReceiptHandle"]}
            for msg in resp["Messages"]
        ]

        resp = sqs_client.delete_message_batch(QueueUrl=queue_url, Entries=entries)

        if len(resp["Successful"]) != len(entries):
            raise RuntimeError(
                f"Failed to delete messages: entries={entries!r} resp={resp!r}"
            )


if __name__ == "__main__":
    try:
        queue_url = sys.argv[1]
    except IndexError:
        queue_url = None

    if queue_url is not None:
        for message in tqdm.tqdm(download_messages(queue_url=queue_url)):
            print(json.dumps(message))
    else:
        for queue_url in list_queue_urls():
            print(queue_url)
