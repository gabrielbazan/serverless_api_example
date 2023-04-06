from typing import Any, Dict

from todos.aws import LambdaResponseKey, get_dynamodb_table
from todos.http import StatusCode
from todos.settings import ListResource


def handler(event: Dict[Any, Any], context: Dict[Any, Any]) -> Dict[str, Any]:
    table = get_dynamodb_table()

    result = table.scan(
        Limit=ListResource.DEFAULT_LIMIT,
    )

    items = result["Items"]

    return {
        LambdaResponseKey.STATUS_CODE: StatusCode.OK,
        LambdaResponseKey.BODY: {
            ListResource.Key.RESULTS: items,
            ListResource.Key.COUNT: len(items),
            ListResource.Key.TOTAL_COUNT: table.item_count,
        },
    }
