from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from todos.aws import AwsResource, ResourceSetting, get_dynamodb_table
from todos.environment import EnvironmentVariable

MODULE = "todos.aws"


class AwsTestCase(TestCase):
    @patch(f"{MODULE}.get_environment_variable_or_raise")
    @patch(f"{MODULE}.boto3")
    def test_get_dynamodb_table(
        self, boto3: MagicMock, get_environment_variable_or_raise: MagicMock
    ) -> None:
        # Given
        endpoint_url, table_name = MagicMock(), MagicMock()
        get_environment_variable_or_raise.side_effect = endpoint_url, table_name

        dynamodb = MagicMock()
        boto3.resource.return_value = dynamodb

        table = MagicMock()
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
