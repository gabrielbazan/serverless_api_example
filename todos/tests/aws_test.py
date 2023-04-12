from unittest import TestCase
from unittest.mock import MagicMock, Mock, call, patch

from todos.aws import (
    AwsResource,
    ResourceSetting,
    error_is,
    get_dynamodb_table,
    get_error_code,
)
from todos.environment import EnvironmentVariable

MODULE = "todos.aws"


class AwsTestCase(TestCase):
    @patch(f"{MODULE}.get_environment_variable_or_raise")
    @patch(f"{MODULE}.boto3")
    def test_get_dynamodb_table(
        self, boto3: Mock, get_environment_variable_or_raise: Mock
    ) -> None:
        # Given
        endpoint_url, table_name = Mock(), Mock()
        get_environment_variable_or_raise.side_effect = endpoint_url, table_name

        dynamodb = Mock()
        boto3.resource.return_value = dynamodb

        table = Mock()
        dynamodb.Table.return_value = table

        # When
        dynamodb_table = get_dynamodb_table()

        # Then
        get_environment_variable_or_raise.assert_has_calls(
            [
                call(EnvironmentVariable.AWS_ENDPOINT_URL),
                call(EnvironmentVariable.DYNAMODB_TABLE),
            ]
        )

        boto3.resource.assert_called_once_with(
            AwsResource.DYNAMODB,
            **{
                ResourceSetting.ENDPOINT_URL: endpoint_url,
            },
        )

        dynamodb.Table.assert_called_once_with(table_name)

        self.assertIs(dynamodb_table, table)

    def test_get_error_code(self) -> None:
        # Given
        code = Mock()
        error_info = Mock()
        error = Mock()

        error_info.get.return_value = code
        error.response.get.return_value = error_info

        # When
        returned_code = get_error_code(error)

        # Then
        self.assertIs(code, returned_code)

    @patch(f"{MODULE}.get_error_code")
    def test_error_is(self, get_error_code: MagicMock) -> None:
        # Given
        error = Mock()
        error_code = "code"
        get_error_code.return_value = "code"

        # When
        errrors_match = error_is(error, error_code)

        # Then
        get_error_code.assert_called_once_with(error)
        self.assertTrue(errrors_match)
