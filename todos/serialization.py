import json
from typing import Any, Dict, Optional, Tuple

from pydantic.error_wrappers import ValidationError

from todos.aws import Lambda
from todos.http import StatusCode
from todos.settings import ERROR_RESPONSE_KEY


def validate_request_body(
    event: Dict[str, Any], model: Any
) -> Tuple[Any, Optional[Dict[str, Any]]]:
    try:
        body = json.loads(event[Lambda.Event.BODY])
        data = model(**body).to_dict()
        return data, None
    except ValidationError as e:
        errors = build_error_response(StatusCode.BAD_REQUEST, e.errors())
        return None, errors


def build_error_response(status_code: int, error: Any) -> Dict[str, Any]:
    return build_response(status_code, {ERROR_RESPONSE_KEY: error})


def build_response(status_code: int, body: Any) -> Dict[str, Any]:
    return {Lambda.Response.STATUS_CODE: status_code, Lambda.Response.BODY: body}
