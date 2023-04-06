import json
import logging
import time
import uuid

from todos.aws import get_dynamodb_table


def handler(event, context):
    data = json.loads(event["body"])

    if "text" not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")

    timestamp = str(time.time())

    table = get_dynamodb_table()

    item = {
        "id": str(uuid.uuid1()),
        "text": data["text"],
        "checked": False,
        "createdAt": timestamp,
        "updatedAt": timestamp,
    }

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps(item),
    }
