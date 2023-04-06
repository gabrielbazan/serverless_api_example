import json
from typing import Dict

from todos.aws import LambdaResponseKey, get_dynamodb_table
from todos.http import StatusCode


def handler(event: Dict, context: Dict) -> Dict:
    table = get_dynamodb_table()

    result = table.get_item(Key={"id": event["pathParameters"]["id"]})

    return {
        LambdaResponseKey.STATUS_CODE: StatusCode.OK,
        LambdaResponseKey.BODY: json.dumps(result["Item"]),
    }
