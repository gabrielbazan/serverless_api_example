from boto3 import resource

from todos.environment import EnvironmentVariable, get_environment_variable_or_raise


class AwsResource:
    DYNAMODB: str = "dynamodb"


class AwsResourceSetting:
    ENDPOINT_URL: str = "endpoint_url"


class LambdaResponseKey:
    STATUS_CODE = "statusCode"
    BODY: str = "body"


def get_dynamodb_table():
    endpoint_url = get_environment_variable_or_raise(
        EnvironmentVariable.AWS_ENDPOINT_URL,
    )
    table_name = get_environment_variable_or_raise(
        EnvironmentVariable.DYNAMODB_TABLE,
    )

    dynamodb = resource(
        AwsResource.DYNAMODB,
        **{
            AwsResourceSetting.ENDPOINT_URL: endpoint_url,
        },
    )

    return dynamodb.Table(table_name)
