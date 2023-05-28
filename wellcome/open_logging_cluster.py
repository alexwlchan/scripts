#!/usr/bin/env python3
"""
Open an app’s logs in the logging cluster.

This script will:

1.  Query the logging cluster for all ECS service/cluster names and all
    Lambda function names

2.  Offer them to the user as a pick list

3.  When the user selects an item, open Kibana in their web browser with
    appropriate filters for the selected item

"""

import json
import os
import sys
import webbrowser

import boto3  # boto3==1.24.85
import httpx  # httpx==0.24.1
from iterfzf import iterfzf  # iterfzf==0.5.0.20.0


# Where to cache data between runs.
#
# Because running the ES query is moderately slow, the script caches
# lookups here -- this allows the user to start selecting an item before
# the latest data is loaded from Elasticsearch.
CACHE_FILE = os.path.join(os.environ["HOME"], ".logging_cluster.json")


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


def get_secret_string(sess, **kwargs):
    """
    Look up a SecretString from Secrets Manager, and return the string.
    """
    secrets = sess.client("secretsmanager")

    resp = secrets.get_secret_value(**kwargs)

    return resp["SecretString"]


def get_logging_options_from_es():
    sess = get_aws_session(role_arn="arn:aws:iam::760097843905:role/platform-developer")

    logging_config = {
        key: get_secret_string(sess, SecretId=f"shared/logging/es_{key}")
        for key in ("host", "port", "user", "pass")
    }

    endpoint = f"https://{logging_config['host']}:{logging_config['port']}"

    resp = httpx.request(
        "GET",
        f"{endpoint}/service-logs-*/_search",
        auth=(logging_config["user"], logging_config["pass"]),
        json={
            "size": 0,
            "aggs": {
                "ecs_services": {
                    "terms": {"field": "service_name.keyword", "size": 1000},
                    "aggs": {
                        "ecs_cluster": {
                            "terms": {"field": "ecs_cluster.keyword", "size": 1}
                        }
                    },
                },
                "lambdas": {"terms": {"field": "service.keyword", "size": 100}},
            },
        },
    ).json()

    result = {}

    for bucket in resp["aggregations"]["ecs_services"]["buckets"]:
        service_name = bucket["key"]
        cluster_name = bucket["ecs_cluster"]["buckets"][0]["key"]
        label = f"{service_name} ({cluster_name})"

        result[cluster_name] = {
            "type": "ecs_cluster",
            "cluster_name": cluster_name,
        }

        result[label] = {
            "type": "ecs_service",
            "service_name": service_name,
            "cluster_name": cluster_name,
        }

    for bucket in resp["aggregations"]["lambdas"]["buckets"]:
        function_name = bucket["key"]
        result[function_name] = {
            "type": "lambda",
            "function_name": function_name,
        }

    return result


def get_logging_options():
    try:
        with open(CACHE_FILE) as infile:
            cached_entries = json.load(infile)
    except FileNotFoundError:
        cached_entries = {}

    yield from cached_entries.items()

    new_entries = get_logging_options_from_es()

    for k, v in new_entries.items():
        if k not in cached_entries:
            yield (k, v)

    updated_entries = {**cached_entries, **new_entries}

    with open(CACHE_FILE, "w") as outfile:
        outfile.write(json.dumps(updated_entries, indent=2, sort_keys=True))


if __name__ == "__main__":
    choice = iterfzf(label for (label, _) in get_logging_options())

    if choice is None:
        sys.exit(0)

    with open(CACHE_FILE) as infile:
        es_info = json.load(infile)[choice]

    if es_info["type"] == "ecs_service":
        cluster_name = es_info["cluster_name"]
        service_name = es_info["service_name"]

        url = f"https://logging.wellcomecollection.org/app/discover#/?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-15m,to:now))&_a=(columns:!(log),filters:!(('$state':(store:appState),meta:(alias:!n,disabled:!f,index:cb5ba262-ec15-46e3-a4c5-5668d65fe21f,key:ecs_cluster,negate:!f,params:(query:{cluster_name}),type:phrase),query:(match_phrase:(ecs_cluster:{cluster_name}))),('$state':(store:appState),meta:(alias:!n,disabled:!f,index:cb5ba262-ec15-46e3-a4c5-5668d65fe21f,key:service_name,negate:!f,params:(query:{service_name}),type:phrase),query:(match_phrase:(service_name:{service_name})))),index:cb5ba262-ec15-46e3-a4c5-5668d65fe21f,interval:auto,query:(language:kuery,query:''),sort:!(!('@timestamp',desc)))"
    elif es_info["type"] == "ecs_cluster":
        cluster_name = es_info["cluster_name"]
        url = f"https://logging.wellcomecollection.org/app/discover#/?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-15m,to:now))&_a=(columns:!(service_name,log),filters:!(('$state':(store:appState),meta:(alias:!n,disabled:!f,index:cb5ba262-ec15-46e3-a4c5-5668d65fe21f,key:ecs_cluster,negate:!f,params:(query:{cluster_name}),type:phrase),query:(match_phrase:(ecs_cluster:{cluster_name})))),index:cb5ba262-ec15-46e3-a4c5-5668d65fe21f,interval:auto,query:(language:kuery,query:''),sort:!(!('@timestamp',desc)))"
    elif es_info["type"] == "lambda":
        function_name = es_info["function_name"].replace("/", "%2F")
        url = f"https://logging.wellcomecollection.org/app/discover#/?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-15m,to:now))&_a=(columns:!(log),filters:!(('$state':(store:appState),meta:(alias:!n,disabled:!f,index:cb5ba262-ec15-46e3-a4c5-5668d65fe21f,key:service,negate:!f,params:(query:{function_name}),type:phrase),query:(match_phrase:(service:{function_name})))),index:cb5ba262-ec15-46e3-a4c5-5668d65fe21f,interval:auto,query:(language:kuery,query:''),sort:!(!('@timestamp',desc)))"

    webbrowser.open(url)
