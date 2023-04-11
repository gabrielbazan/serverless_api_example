from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from todos.environment import get_environment_variable_or_raise

MODULE = "todos.environment"


class EnvironmentTestCase(TestCase):
    @patch(f"{MODULE}.environ")
    def test_get_environment_variable_or_raise_when_variable_is_defined(
        self, environ: MagicMock
    ) -> None:
        # Given
        variable_name = Mock()
        value = Mock()

        environ.__contains__.return_value = True
        environ.__getitem__.return_value = value

        # When
        returned_value = get_environment_variable_or_raise(variable_name)

        # Then
        environ.__contains__.assert_called_once_with(variable_name)
        environ.__getitem__.assert_called_once_with(variable_name)
        self.assertIs(returned_value, value)

    @patch(f"{MODULE}.environ")
    def test_get_environment_variable_or_raise_when_variable_is_not_defined(
        self, environ: MagicMock
    ) -> None:
        # Given
        variable_name = Mock()

        environ.__contains__.return_value = False

        # When, then
        with self.assertRaises(AssertionError):
            get_environment_variable_or_raise(variable_name)

        environ.__contains__.assert_called_once_with(variable_name)
