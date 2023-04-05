from .aws import get_dynamodb_table


def handler(event, context):
    table = get_dynamodb_table()

    table.delete_item(Key={"id": event["pathParameters"]["id"]})

    return {
        "statusCode": 204,
        "body": "",
    }
