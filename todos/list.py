import json
import os

import boto3

client = boto3.client(
    "dynamodb",
    endpoint_url=os.environ["AWS_ENDPOINT_URL"],
)


def handler(event, context):
    result = client.scan(TableName=os.environ["DYNAMODB_TABLE"])

    return {
        "statusCode": 200,
        "body": json.dumps(result["Items"]),
    }
