from typing import Any

import boto3
from botocore.exceptions import ClientError

from todos.environment import EnvironmentVariable, get_environment_variable_or_raise


class AwsResource:
    DYNAMODB: str = "dynamodb"


class ResourceSetting:
    ENDPOINT_URL: str = "endpoint_url"


class Lambda:
    class Event:
        BODY: str = "body"
        PATH_PARAMETERS: str = "pathParameters"

    class Response:
        STATUS_CODE = "statusCode"
        BODY: str = "body"


class Dynamo:
    class Scan:
        class Response:
            ITEMS: str = "Items"

    class PutItem:
        class Request:
            ITEM: str = "Item"

    class GetItem:
        class Request:
            KEY: str = "Key"

        class Response:
            ITEM: str = "Item"

    class UpdateItem:
        class Response:
            ATTRIBUTES: str = "Attributes"


class Error:
    CONDITIONAL_CHECK_FAILED = "ConditionalCheckFailedException"


def error_is(e: ClientError, error_code: str) -> bool:
    return bool(get_error_code(e) == error_code)


def get_error_code(e: ClientError) -> Any:
    return e.response.get("Error", {}).get("Code")


def get_dynamodb_table() -> Any:
    endpoint_url = get_environment_variable_or_raise(
        EnvironmentVariable.AWS_ENDPOINT_URL,
    )
    table_name = get_environment_variable_or_raise(
        EnvironmentVariable.DYNAMODB_TABLE,
    )

    dynamodb = boto3.resource(
        AwsResource.DYNAMODB,
        **{
            ResourceSetting.ENDPOINT_URL: endpoint_url,
        },
    )

    return dynamodb.Table(table_name)
