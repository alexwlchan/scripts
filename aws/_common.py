#!/usr/bin/env python3

import boto3
import hyperlink


ACCOUNT_NAMES = {
    "760097843905": "platform",
    "299497370133": "workflow",
}


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


def guess_account(s3_identifier):
    """
    Given the name of an S3 bucket, guess the account it belongs to.

    You can pass the name of the bucket, or the S3 URI.

    Examples:

        > guess_account('s3://example-bucket/cat.jpg')
        {'account_id': '1234567890', 'name': 'example'}

        > guess_account('example-bucket')
        {'account_id': '1234567890', 'name': 'example'}

    """
    if "wellcomedigitalworkflow" in s3_identifier:
        account_id = '299497370133'
    else:
        return None

    account_name = ACCOUNT_NAMES[account_id]

    return {
        "account_id": account_id,
        "name": account_name,
        "role_arn": f"arn:aws:iam::{account_id}:role/{account_name}-read_only",
    }


def create_s3_session(s3_identifier):
    account = guess_account(s3_identifier)
    if account:
        return get_aws_session(role_arn=account["role_arn"])
    else:
        return boto3.Session()


def parse_s3_uri(s3_uri):
    uri = hyperlink.URL.from_text(s3_uri)

    if uri.scheme != "s3":
        raise ValueError(f"Unrecognised scheme in {s3_uri!r}, expected s3://")

    bucket = uri.host
    prefix = "/".join(uri.path)

    return {"Bucket": bucket, "Prefix": prefix}
