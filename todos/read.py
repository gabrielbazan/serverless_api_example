from typing import Any, Dict

from todos.aws import Dynamo, Lambda, get_dynamodb_table
from todos.http import StatusCode
from todos.serialization import build_error_response, build_response
from todos.settings import DYNAMODB_TABLE_KEY


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    item_id = event[Lambda.Event.PATH_PARAMETERS][DYNAMODB_TABLE_KEY]

    table = get_dynamodb_table()

    result = table.get_item(
        **{
            Dynamo.GetItem.Request.KEY: {
                DYNAMODB_TABLE_KEY: item_id,
            }
        }
    )

    item = result.get(Dynamo.GetItem.Response.ITEM)

    if not item:
        return build_error_response(StatusCode.NOT_FOUND, "The item does not exist")

    return build_response(StatusCode.OK, item)
