from os import environ


class EnvironmentVariable:
    AWS_ENDPOINT_URL = "AWS_ENDPOINT_URL"
    DYNAMODB_TABLE = "DYNAMODB_TABLE"


def get_environment_variable_or_raise(name: str) -> str:
    assert name in environ, f"{name} environment variable is not set"
    return environ[name]
