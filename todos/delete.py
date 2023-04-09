from typing import Any, Dict

from botocore.exceptions import ClientError

from todos.aws import Error, Lambda, error_is, get_dynamodb_table
from todos.http import StatusCode
from todos.serialization import build_error_response, build_response
from todos.settings import DYNAMODB_TABLE_KEY


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    item_id = event[Lambda.Event.PATH_PARAMETERS][DYNAMODB_TABLE_KEY]

    try:
        get_dynamodb_table().delete_item(
            Key={DYNAMODB_TABLE_KEY: item_id},
            ConditionExpression=f"attribute_exists({DYNAMODB_TABLE_KEY})",
        )

        return build_response(StatusCode.NO_CONTENT, "")
    except ClientError as e:
        if error_is(e, Error.CONDITIONAL_CHECK_FAILED):
            return build_error_response(StatusCode.NOT_FOUND, "The item does not exist")

        raise
