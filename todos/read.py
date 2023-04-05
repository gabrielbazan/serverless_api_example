import json

from .aws import get_dynamodb_table


def handler(event, context):
    table = get_dynamodb_table()

    result = table.get_item(Key={"id": event["pathParameters"]["id"]})

    return {
        "statusCode": 200,
        "body": json.dumps(result["Item"]),
    }
