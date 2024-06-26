#!/usr/bin/env python3
"""
Print the items in a DynamoDB table as JSON objects.  If no table name is
supplied, it prints a list of all table names in the account.

You can do something similar with `aws dynamodb scan`, but this script
has a couple of neat features:

-   It does a Parallel Scan instead of a vanilla Scan, so it's faster
-   It starts returning objects immediately, rather than waiting until
    it scans the whole table
-   The output format is more convenient -- a single JSON object per line,
    so it can be used with text utilities like `head` and `tail`, and the
    DynamoD JSON representation (e.g. {"sides": {"N": "5"}}) is transformed
    into a more useful form (e.g. {"sides": 5})

See https://alexwlchan.net/2020/getting-every-item-from-a-dynamodb-table-with-python/

"""

import concurrent.futures
import decimal
import json
import itertools
import sys

import boto3
import tqdm


def is_integer(d: decimal.Decimal):
    _, denominator = d.as_integer_ratio()
    return denominator == 1


class DynamoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal) and is_integer(obj):
            return int(obj)


def parallel_scan_table(sess, *, TableName, **kwargs):
    """
    Generates all the items in a DynamoDB table.

    :param dynamo_client: A boto3 client for DynamoDB.
    :param TableName: The name of the table to scan.

    Other keyword arguments will be passed directly to the Scan operation.
    See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan

    This does a Parallel Scan operation over the table.

    """
    dynamo_client = sess.resource("dynamodb").meta.client

    # How many segments to divide the table into?  As long as this is >= to the
    # number of threads used by the ThreadPoolExecutor, the exact number doesn't
    # seem to matter.
    total_segments = 25

    # How many scans to run in parallel?  If you set this really high you could
    # overwhelm the table read capacity, but otherwise I don't change this much.
    max_scans_in_parallel = 5

    # Schedule an initial scan for each segment of the table.  We read each
    # segment in a separate thread, then look to see if there are more rows to
    # read -- and if so, we schedule another scan.
    tasks_to_do = [
        {
            **kwargs,
            "TableName": TableName,
            "Segment": segment,
            "TotalSegments": total_segments,
        }
        for segment in range(total_segments)
    ]

    # Make the list an iterator, so the same tasks don't get run repeatedly.
    scans_to_run = iter(tasks_to_do)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Schedule the initial batch of futures.  Here we assume that
        # max_scans_in_parallel < total_segments, so there's no risk that
        # the queue will throw an Empty exception.
        futures = {
            executor.submit(dynamo_client.scan, **scan_params): scan_params
            for scan_params in itertools.islice(scans_to_run, max_scans_in_parallel)
        }

        while futures:
            # Wait for the first future to complete.
            done, _ = concurrent.futures.wait(
                futures, return_when=concurrent.futures.FIRST_COMPLETED
            )

            for fut in done:
                yield from fut.result()["Items"]

                scan_params = futures.pop(fut)

                # A Scan reads up to N items, and tells you where it got to in
                # the LastEvaluatedKey.  You pass this key to the next Scan operation,
                # and it continues where it left off.
                try:
                    scan_params["ExclusiveStartKey"] = fut.result()["LastEvaluatedKey"]
                except KeyError:
                    break
                tasks_to_do.append(scan_params)

            # Schedule the next batch of futures.  At some point we might run out
            # of entries in the queue if we've finished scanning the table, so
            # we need to spot that and not throw.
            for scan_params in itertools.islice(scans_to_run, len(done)):
                futures[executor.submit(dynamo_client.scan, **scan_params)] = (
                    scan_params
                )


def list_table_names(sess):
    paginator = sess.client("dynamodb").get_paginator("list_tables")

    for page in paginator.paginate():
        yield from page["TableNames"]


if __name__ == "__main__":
    try:
        table_name = sys.argv[1]
    except IndexError:
        table_name = None

    sess = boto3.Session()

    if table_name is not None:
        for item in tqdm.tqdm(parallel_scan_table(sess, TableName=table_name)):
            print(json.dumps(item, cls=DynamoEncoder))
    else:
        for table_name in list_table_names(sess):
            print(table_name)
