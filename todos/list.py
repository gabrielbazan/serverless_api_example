import json

from todos.aws import get_dynamodb_table


def handler(event, context):
    table = get_dynamodb_table()

    result = table.scan()

    return {
        "statusCode": 200,
        "body": json.dumps(result["Items"]),
    }
