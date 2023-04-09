from typing import Any, Dict

from todos.aws import Dynamo, get_dynamodb_table
from todos.http import StatusCode
from todos.serialization import build_response
from todos.settings import ListResource


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    table = get_dynamodb_table()

    result = table.scan(Limit=ListResource.DEFAULT_LIMIT)

    items = result[Dynamo.Scan.Response.ITEMS]

    return build_response(
        StatusCode.OK,
        {
            ListResource.Key.RESULTS: items,
            ListResource.Key.COUNT: len(items),
            ListResource.Key.TOTAL_COUNT: table.item_count,
        },
    )
