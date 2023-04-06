import json
import logging
from typing import Any, Dict

from todos.aws import LambdaResponseKey, get_dynamodb_table
from todos.http import StatusCode
from todos.utils import get_current_utc_time


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    data = json.loads(event["body"])

    if "text" not in data or "checked" not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")

    table = get_dynamodb_table()

    result = table.update_item(
        Key={"id": event["pathParameters"]["id"]},
        ExpressionAttributeNames={
            "#todo_text": "text",
        },
        ExpressionAttributeValues={
            ":text": data["text"],
            ":checked": data["checked"],
            ":updatedAt": get_current_utc_time(),
        },
        UpdateExpression="SET #todo_text = :text, "
        "checked = :checked, "
        "updatedAt = :updatedAt",
        ReturnValues="ALL_NEW",
    )

    return {
        LambdaResponseKey.STATUS_CODE: StatusCode.OK,
        LambdaResponseKey.BODY: json.dumps(result["Attributes"]),
    }
