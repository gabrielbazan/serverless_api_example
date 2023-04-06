from typing import Dict

from todos.aws import LambdaResponseKey, get_dynamodb_table
from todos.http import StatusCode
from todos.settings import ListResource


def handler(event: Dict, context: Dict) -> Dict:
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
