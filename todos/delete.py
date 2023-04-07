from typing import Any, Dict

from todos.aws import Lambda, get_dynamodb_table
from todos.http import StatusCode


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    table = get_dynamodb_table()

    table.delete_item(Key={"id": event["pathParameters"]["id"]})

    return {
        Lambda.Response.STATUS_CODE: StatusCode.NO_CONTENT,
        Lambda.Response.BODY: "",
    }
