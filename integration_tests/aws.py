from typing import Any

import boto3

AWS_ENDPOINT_URL = "http://localhost:4566"
AWS_REGION_NAME = "us-east-1"
AWS_ACCESS_KEY_ID = "dummy_access_key"
AWS_SECRET_ACCESS_KEY = "dummy_secret_acces_key"

REST_API_URL_TEMPLATE = f"{AWS_ENDPOINT_URL}/restapis/{{}}/local/_user_request_"


def query_rest_api_url() -> str:
    api_id = query_rest_api_id()
    return build_rest_api_url(api_id)


def query_rest_api_id() -> str:
    gateway = get_aws_client("apigateway")

    response = gateway.get_rest_apis()

    rest_apis = response["items"]

    assert rest_apis, "No REST APIs found"
    assert len(rest_apis) == 1, "More than one REST API found"

    rest_api = rest_apis[0]

    return str(rest_api["id"])


def build_rest_api_url(api_id: str) -> str:
    return REST_API_URL_TEMPLATE.format(api_id)


def get_aws_client(name: str) -> Any:
    return boto3.client(
        name,
        endpoint_url=AWS_ENDPOINT_URL,
        region_name=AWS_REGION_NAME,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
