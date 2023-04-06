from typing import Any, Dict

from todos.aws import LambdaResponseKey, get_dynamodb_table
from todos.http import StatusCode


def handler(event: Dict[Any, Any], context: Dict[Any, Any]) -> Dict[str, Any]:
    table = get_dynamodb_table()

    table.delete_item(Key={"id": event["pathParameters"]["id"]})

    return {
        LambdaResponseKey.STATUS_CODE: StatusCode.NO_CONTENT,
        LambdaResponseKey.BODY: "",
    }
