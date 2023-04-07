import json
from typing import Any, Dict

from todos.aws import Lambda
from todos.http import StatusCode


def validate_request_body(event: Dict[str, Any], model: Any) -> Any:
    try:
        body = json.loads(event[Lambda.Event.BODY])
        return model(**body).to_dict()
    except Exception:
        return {
            Lambda.Response.BODY: {"error": "Malformed request body"},
            Lambda.Response.STATUS_CODE: StatusCode.BAD_REQUEST,
        }
