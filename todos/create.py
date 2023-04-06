import json
import logging
import uuid
from typing import Any, Dict

from todos.aws import LambdaResponseKey, get_dynamodb_table
from todos.http import StatusCode
from todos.utils import get_current_utc_time


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    data = json.loads(event["body"])

    if "text" not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")

    now = get_current_utc_time()

    item = {
        "id": str(uuid.uuid1()),
        "text": data["text"],
        "checked": False,
        "createdAt": now,
        "updatedAt": now,
    }

    table = get_dynamodb_table()
    table.put_item(Item=item)

    return {
        LambdaResponseKey.STATUS_CODE: StatusCode.OK,
        LambdaResponseKey.BODY: item,
    }
