from typing import Any

import boto3

from todos.environment import EnvironmentVariable, get_environment_variable_or_raise


class AwsResource:
    DYNAMODB: str = "dynamodb"


class AwsResourceSetting:
    ENDPOINT_URL: str = "endpoint_url"


class LambdaResponseKey:
    STATUS_CODE = "statusCode"
    BODY: str = "body"


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
            AwsResourceSetting.ENDPOINT_URL: endpoint_url,
        },
    )

    print("dynamodb.Table(table_name): ", dynamodb.Table(table_name))

    return dynamodb.Table(table_name)
