#!/usr/bin/env python3
"""
Print a summary of messages visible on our SQS queues (and dead-letter queues).

    $ sqs_stats
        1        -	calm-windows
        -        3	catalogue-2023-03-29_image_inferrer_input
        -    1,246	catalogue-2023-03-29_ingestor_works_input
        1        -	sierra-adapter-20200604-sierra_bibs_windows

Note: this relies on a Wellcome-specific convention that the dead-letter queue
associated with a queue has the same name but with `_dlq` on the end,
e.g. `calm-windows` and `calm-windows_dlq`.

"""

import collections
import os
import sys

import boto3
import humanize
import termcolor

from _common import create_link_text

# https://github.com/alexwlchan/concurrently
sys.path.append(os.path.join(os.environ["HOME"], "repos", "concurrently"))

from concurrently import concurrently  # noqa: E402


def list_queue_urls_in_account(sess, *, prefixes):
    """
    Generates a list of all the queue URLs in an account.
    """
    sqs_client = sess.client("sqs")

    for prefix in prefixes:
        for page in sqs_client.get_paginator("list_queues").paginate(
            QueueNamePrefix=prefix
        ):
            yield from page["QueueUrls"]


def get_queue_stats(sess, *, queue_urls):
    """
    Get the size of the queues associated with this pipeline.
    """
    sqs_client = sess.client("sqs")

    attribute_names = [
        "ApproximateNumberOfMessages",
        "ApproximateNumberOfMessagesNotVisible",
        "ApproximateNumberOfMessagesDelayed",
    ]

    queue_responses = {}

    for q_url, q_resp in concurrently(
        handler=lambda q_url: sqs_client.get_queue_attributes(
            QueueUrl=q_url, AttributeNames=attribute_names
        ),
        inputs=queue_urls
    ):
        queue_responses[q_url] = q_resp

    return {
        q_url: sum(int(resp["Attributes"][attr]) for attr in attribute_names)
        for q_url, resp in queue_responses.items()
    }


def print_number(account_id, region_name, queue_name, *, value, color):
    if value is None:
        print("-".rjust(9, " "), end="")
    else:
        spaces_required = 9 - len(humanize.intcomma(value))

        print(
            termcolor.colored(
                " " * spaces_required + create_link_text(
                    url=f"https://{region_name}.console.aws.amazon.com/sqs/v2/home?region={region_name}#/queues/https%3A%2F%2Fsqs.{region_name}.amazonaws.com%2F{account_id}%2F{queue_name}",
                    label=humanize.intcomma(value),
                ),
                color,
            ),
            end="",
        )


def pprint_queue_stats(account_id, region_name, queue_stats):
    interesting_queues = {
        q_url: q_size for q_url, q_size in queue_stats.items() if q_size > 0
    }

    if not interesting_queues:
        print("All queues are empty")
        return

    paired_queues = collections.defaultdict(lambda: {"q": None, "dlq": None})

    for q_url, q_size in interesting_queues.items():
        q_name = q_url.split("/")[-1]
        if q_name.endswith("_dlq"):
            paired_queues[q_name.replace("_dlq", "")]["dlq"] = q_size
        else:
            paired_queues[q_name]["q"] = q_size

    for q_name, q_stats in sorted(paired_queues.items()):
        print_number(account_id, region_name, q_name, value=q_stats["q"], color="green")
        print_number(
            account_id, region_name, q_name + "_dlq", value=q_stats["dlq"], color="red"
        )
        print("\t", end="")
        print(q_name)


if __name__ == "__main__":
    sess = boto3.Session()

    prefixes = sys.argv[1:] or ("",)

    queue_urls = list_queue_urls_in_account(sess, prefixes=prefixes)

    queue_stats = get_queue_stats(sess, queue_urls=queue_urls)

    sts = sess.client("sts")
    account_id = sts.get_caller_identity()["Account"]
    region_name = sess.region_name

    pprint_queue_stats(account_id, region_name, queue_stats)
