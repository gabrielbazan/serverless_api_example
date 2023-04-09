from typing import Any, Dict

from todos.aws import Dynamo, get_dynamodb_table
from todos.http import StatusCode
from todos.models import ToDoCreation
from todos.serialization import build_response, validate_request_body


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    data, errors = validate_request_body(event, ToDoCreation)

    if errors:
        return errors

    get_dynamodb_table().put_item(**{Dynamo.PutItem.Request.ITEM: data})

    return build_response(StatusCode.OK, data)
