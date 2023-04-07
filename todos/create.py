from typing import Any, Dict

from todos.aws import Lambda, get_dynamodb_table
from todos.http import StatusCode
from todos.models import ToDoCreation
from todos.validation import validate_request_body


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    data = validate_request_body(event, ToDoCreation)

    get_dynamodb_table().put_item(Item=data)

    return {
        Lambda.Response.STATUS_CODE: StatusCode.OK,
        Lambda.Response.BODY: data,
    }
