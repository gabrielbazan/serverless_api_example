from typing import Any, Dict

from botocore.exceptions import ClientError

from todos.aws import Dynamo, Error, Lambda, error_is, get_dynamodb_table
from todos.http import StatusCode
from todos.models import ToDoUpdate
from todos.serialization import (
    build_error_response,
    build_response,
    validate_request_body,
)
from todos.settings import DYNAMODB_TABLE_KEY


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    item_id = event[Lambda.Event.PATH_PARAMETERS][DYNAMODB_TABLE_KEY]

    data, errors = validate_request_body(event, ToDoUpdate)

    if errors:
        return errors

    try:
        table = get_dynamodb_table()

        result = table.update_item(
            Key={DYNAMODB_TABLE_KEY: item_id},
            ConditionExpression=f"attribute_exists({DYNAMODB_TABLE_KEY})",
            ExpressionAttributeValues=build_expression_attribute_values(data),
            UpdateExpression=build_update_expression(data),
            ReturnValues="ALL_NEW",
        )

        return build_response(
            StatusCode.OK,
            result[Dynamo.UpdateItem.Response.ATTRIBUTES],
        )
    except ClientError as e:
        if error_is(e, Error.CONDITIONAL_CHECK_FAILED):
            return build_error_response(StatusCode.NOT_FOUND, "The item does not exist")

        raise


def build_update_expression(data: Dict[str, Any]) -> str:
    expression = "SET "

    for key, value in data.items():
        if value is not None:
            expression += f"{key} = :{key}, "

    expression = expression[:-2]

    return expression


def build_expression_attribute_values(data: Dict[str, Any]) -> Dict[str, Any]:
    return {f":{key}": value for key, value in data.items() if value is not None}
